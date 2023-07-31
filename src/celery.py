from celery import Celery

from src import settings


def create_celery_app() -> Celery:
    _app = Celery('celery_worker')
    _app.config_from_object(settings)
    _app.autodiscover_tasks(['src.apps.tasks'])
    return _app


celery_app = create_celery_app()
