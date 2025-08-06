"""Celery worker configuration and tasks for the project."""

import os

from celery import Celery
from celery.schedules import crontab


celery_app = Celery("mp_worker")

# Allow broker and backend URLs to be configured via environment variables
celery_app.conf.broker_url = os.environ.get(
    "CELERY_BROKER_URL", "redis://localhost:6379/0"
)
celery_app.conf.result_backend = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379/0"
)


@celery_app.task
def start_spider() -> str:
    """Run the sample Scrapy spider."""
    from scrapy.crawler import CrawlerProcess

    from app.scraping.sample_spider import SampleSpider

    process = CrawlerProcess(settings={"LOG_ENABLED": False})
    process.crawl(SampleSpider)
    process.start()
    return "spider completed"


@celery_app.task
def process_results() -> str:
    """Process results produced by the spider."""
    # Placeholder for result processing logic
    return "results processed"


# Periodic task configuration using Celery beat
celery_app.conf.beat_schedule = {
    "run-sample-spider": {
        "task": "app.tasks.worker.start_spider",
        "schedule": crontab(minute=0, hour="*"),
    },
    "process-scraped-results": {
        "task": "app.tasks.worker.process_results",
        "schedule": crontab(minute=30, hour="*"),
    },
}

celery_app.conf.timezone = "UTC"


@celery_app.task
def example_task() -> str:
    """Simple example task used for testing."""
    return "task completed"
