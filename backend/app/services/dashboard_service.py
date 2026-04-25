from ..db import repository


def get_dashboard(user_id):
    return repository.get_dashboard_metrics(user_id)
