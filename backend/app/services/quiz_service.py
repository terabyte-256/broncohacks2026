from ..db import repository
from ..utils.errors import ApiError
from ..utils.validation import parse_int


PASSING_SCORE = 70.0


def get_quiz(quiz_id):
    quiz = repository.get_quiz_with_questions(quiz_id)
    if quiz is None:
        raise ApiError("Quiz not found.", status_code=404)
    return quiz


def _normalize_answers(payload_answers):
    if not isinstance(payload_answers, list) or not payload_answers:
        raise ApiError("answers must be a non-empty list.", status_code=400)

    answers = {}
    for item in payload_answers:
        if not isinstance(item, dict):
            raise ApiError("Each answer must be an object.", status_code=400)
        if "questionId" not in item or "optionId" not in item:
            raise ApiError(
                "Each answer requires questionId and optionId.",
                status_code=400,
            )

        question_id = parse_int(item.get("questionId"), "questionId", minimum=1)
        option_id = parse_int(item.get("optionId"), "optionId", minimum=1)
        answers[question_id] = option_id

    return answers


def submit_quiz(quiz_id, user_id, payload):
    quiz = get_quiz(quiz_id)
    answers = _normalize_answers(payload.get("answers"))

    correct_map = repository.get_correct_options_for_quiz(quiz_id)
    if not correct_map:
        raise ApiError("Quiz has no answer key configured.", status_code=500)

    unknown_question_ids = [qid for qid in answers if qid not in correct_map]
    if unknown_question_ids:
        raise ApiError(
            "Answer payload references unknown question IDs.",
            status_code=400,
            details={"questionIds": sorted(unknown_question_ids)},
        )

    missing_question_ids = [qid for qid in correct_map if qid not in answers]
    if missing_question_ids:
        raise ApiError(
            "All quiz questions must be answered.",
            status_code=400,
            details={"missingQuestionIds": sorted(missing_question_ids)},
        )

    correct_answers = sum(1 for qid, correct_option in correct_map.items() if answers[qid] == correct_option)
    total_questions = len(correct_map)
    score = round((correct_answers / total_questions) * 100, 2)

    attempt_id = repository.create_quiz_attempt(
        user_id=user_id,
        quiz_id=quiz_id,
        score=score,
        total_questions=total_questions,
        correct_answers=correct_answers,
    )

    module_id = quiz["moduleId"]
    completion_percent = 100.0 if score >= PASSING_SCORE else 60.0
    repository.upsert_progress(user_id, module_id, completion_percent, score)

    if score >= PASSING_SCORE:
        repository.mark_topic_completed(user_id, module_id)

    return {
        "attemptId": attempt_id,
        "score": score,
        "correctAnswers": correct_answers,
        "totalQuestions": total_questions,
        "passed": score >= PASSING_SCORE,
    }
