from ..db import repository
from ..utils.errors import ApiError
from ..utils.validation import parse_float, parse_int


def get_progress(user_id):
    return repository.get_progress_for_user(user_id)


def update_progress(user_id, payload):
    module_id = parse_int(payload.get("moduleId"), "moduleId", minimum=1)
    completion_percent = parse_float(
        payload.get("completionPercent"),
        "completionPercent",
        minimum=0,
        maximum=100,
    )

    if not repository.module_exists(module_id):
        raise ApiError("Module not found.", status_code=404)

    last_score = payload.get("lastScore")
    parsed_last_score = None
    if last_score is not None:
        parsed_last_score = parse_float(last_score, "lastScore", minimum=0, maximum=100)

    repository.upsert_progress(user_id, module_id, completion_percent, parsed_last_score)

    if completion_percent >= 100:
        repository.mark_topic_completed(user_id, module_id)

    updated = repository.get_module_progress(user_id, module_id)
    return {"progress": updated}
