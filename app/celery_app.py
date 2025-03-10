from celery import Celery
from config import Config

def make_celery():
    """Creates and configures the Celery instance."""
    celery = Celery(
        "app",
        broker=Config.CELERY_BROKER_URL,
        backend=Config.CELERY_RESULT_BACKEND,
        include=["app.tasks"]
    )
    
    celery.conf.update(
        task_serializer="json",
        accept_content=["json"],
        timezone="UTC",
        enable_utc=True
    )
    return celery

celery = make_celery()
