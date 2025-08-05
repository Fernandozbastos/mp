from fastapi import FastAPI

from .api.routes import router as api_router

app = FastAPI()

app.include_router(api_router)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Simple health check endpoint."""
    return {"status": "ok"}
