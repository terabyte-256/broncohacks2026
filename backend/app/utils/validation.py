from .errors import ApiError


def require_json(request):
    if not request.is_json:
        raise ApiError("Request body must be valid JSON.", status_code=400)

    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        raise ApiError("JSON payload must be an object.", status_code=400)

    return payload


def require_fields(payload, fields):
    missing = [field for field in fields if field not in payload]
    if missing:
        raise ApiError(
            "Missing required fields.",
            status_code=400,
            details={"missing": missing},
        )


def parse_int(value, field_name, minimum=None, maximum=None):
    try:
        parsed = int(value)
    except (TypeError, ValueError) as exc:
        raise ApiError(f"{field_name} must be an integer.", status_code=400) from exc

    if minimum is not None and parsed < minimum:
        raise ApiError(f"{field_name} must be >= {minimum}.", status_code=400)
    if maximum is not None and parsed > maximum:
        raise ApiError(f"{field_name} must be <= {maximum}.", status_code=400)

    return parsed


def parse_float(value, field_name, minimum=None, maximum=None):
    try:
        parsed = float(value)
    except (TypeError, ValueError) as exc:
        raise ApiError(f"{field_name} must be numeric.", status_code=400) from exc

    if minimum is not None and parsed < minimum:
        raise ApiError(f"{field_name} must be >= {minimum}.", status_code=400)
    if maximum is not None and parsed > maximum:
        raise ApiError(f"{field_name} must be <= {maximum}.", status_code=400)

    return parsed


def parse_non_empty_string(value, field_name, max_length=5000):
    if not isinstance(value, str):
        raise ApiError(f"{field_name} must be a string.", status_code=400)

    stripped = value.strip()
    if not stripped:
        raise ApiError(f"{field_name} cannot be empty.", status_code=400)

    if len(stripped) > max_length:
        raise ApiError(f"{field_name} is too long.", status_code=400)

    return stripped
