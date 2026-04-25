from ..db import repository
from ..utils.errors import ApiError


def get_tracks(user_id):
    return repository.get_tracks_for_user(user_id)


def get_track_modules(track_id, user_id):
    track = repository.get_track(track_id)
    if track is None:
        raise ApiError("Track not found.", status_code=404)

    modules = repository.get_modules_for_track(track_id, user_id)
    return {
        "track": track,
        "modules": modules,
    }
