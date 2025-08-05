from app.tasks.worker import celery_app, example_task


def test_example_task_execution() -> None:
    celery_app.conf.update(
        broker_url="memory://",
        result_backend="cache+memory://",
        task_always_eager=True,
    )
    result = example_task.delay()
    assert result.get(timeout=10) == "task completed"
