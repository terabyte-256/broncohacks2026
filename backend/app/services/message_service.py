from ..db import repository
from ..services import gemini_service


def analyze_and_store_message(user_id, message_text):
    analysis = gemini_service.analyze_message(message_text)
    repository.create_message_analysis_history(user_id, message_text, analysis)
    return analysis


def get_message_history(user_id, limit):
    return repository.get_message_analysis_history(user_id, limit=limit)
