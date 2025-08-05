# mp

Initial project structure for a FastAPI-based application with asynchronous
components, background workers and scraping utilities.

## Structure

```
app/
├── api/            # API routers
├── auth/           # Authentication helpers
├── db/             # Database configuration and base models
├── scraping/       # Scrapy spiders and utilities
├── tasks/          # Celery workers and tasks
├── config.py       # Application settings
└── main.py         # FastAPI application entrypoint
```

## Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the FastAPI app:
   ```bash
   uvicorn app.main:app --reload
   ```
3. Launch the Celery worker:
   ```bash
   # Ensure broker and backend URLs are configured
   export CELERY_BROKER_URL=redis://localhost:6379/0
   export CELERY_RESULT_BACKEND=redis://localhost:6379/0

   celery -A app.tasks.worker.celery_app worker --loglevel=info
   ```
4. (Optional) Start Celery beat for periodic tasks:
   ```bash
   celery -A app.tasks.worker.celery_app beat --loglevel=info
   ```
