import json
import re

from flask import current_app

from ..models.analysis import AnalysisResult
from ..utils.errors import ApiError

VALID_VERDICTS = {"Safe", "Suspicious", "Scam"}
VALID_RISK_LEVELS = {"Low", "Medium", "High"}


PROMPT_TEMPLATE = """
You are a cybersecurity message classifier.
Evaluate the following message and return JSON only.
Allowed verdict values: Safe, Suspicious, Scam.
Allowed riskLevel values: Low, Medium, High.
Strict output keys: verdict, riskLevel, redFlags, explanation, tips.
redFlags and tips must be arrays of strings.
Do not include markdown fences.

Message:
{message}
""".strip()


def _extract_json(text):
    text = text.strip()
    if not text:
        raise ApiError("Gemini returned an empty response.", status_code=502)

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not match:
        raise ApiError("Gemini response did not contain JSON.", status_code=502)

    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError as exc:
        raise ApiError("Gemini response JSON was invalid.", status_code=502) from exc


def _normalize_enum(value, valid_values, fallback):
    if isinstance(value, str):
        stripped = value.strip()
        for candidate in valid_values:
            if stripped.lower() == candidate.lower():
                return candidate
    return fallback


def _normalize_string_list(values, fallback):
    if not isinstance(values, list):
        return fallback

    cleaned = []
    for value in values:
        if isinstance(value, str):
            stripped = value.strip()
            if stripped:
                cleaned.append(stripped)

    return cleaned or fallback


def _normalize_output(raw_payload):
    if not isinstance(raw_payload, dict):
        raise ApiError("Gemini response was not a JSON object.", status_code=502)

    verdict = _normalize_enum(raw_payload.get("verdict"), VALID_VERDICTS, "Suspicious")
    risk_level = _normalize_enum(raw_payload.get("riskLevel"), VALID_RISK_LEVELS, "Medium")
    red_flags = _normalize_string_list(
        raw_payload.get("redFlags"),
        ["No specific red flags were provided."],
    )
    tips = _normalize_string_list(
        raw_payload.get("tips"),
        ["Do not click unknown links.", "Verify the sender before responding."],
    )

    explanation = raw_payload.get("explanation")
    if not isinstance(explanation, str) or not explanation.strip():
        explanation = "The message was analyzed and normalized due to incomplete AI output."

    result = AnalysisResult(
        verdict=verdict,
        riskLevel=risk_level,
        redFlags=red_flags,
        explanation=explanation.strip(),
        tips=tips,
    )
    return result.to_dict()


def analyze_message(message_text):
    api_key = current_app.config.get("GEMINI_API_KEY")
    if not api_key:
        raise ApiError("Gemini API key is not configured.", status_code=503)

    try:
        import google.generativeai as genai
    except ImportError as exc:
        raise ApiError("Gemini SDK is not installed.", status_code=500) from exc

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(current_app.config.get("GEMINI_MODEL", "gemini-1.5-flash"))

    prompt = PROMPT_TEMPLATE.format(message=message_text)

    try:
        response = model.generate_content(prompt)
    except Exception as exc:
        raise ApiError(
            "Gemini request failed.",
            status_code=502,
            details={"providerError": str(exc)},
        ) from exc

    raw_payload = _extract_json(getattr(response, "text", ""))
    return _normalize_output(raw_payload)
