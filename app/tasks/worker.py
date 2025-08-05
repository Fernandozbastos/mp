from celery import Celery

celery_app = Celery(
    "mp_worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)


@celery_app.task
def example_task() -> str:
    """A simple Celery task example."""
    return "task completed"
