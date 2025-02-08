import logging
from fastapi import status, FastAPI

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from app.middlewares import setup_middlewares
from app.routes.webhook import webhook_route
from app.settings.logging import LOGGING_CONFIG
from app.settings.tracing import setup_tracer


def main() -> FastAPI:
    logger = logging.getLogger(__name__)
    logger.info({"message": "Initializing FastAPI app"})

    tracer = setup_tracer()

    app = FastAPI()

    setup_middlewares(app, logger)

    FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer)
    app.include_router(webhook_route)

    @app.get("/healthcheck", status_code=status.HTTP_200_OK)
    def healthcheck() -> dict:
        return {"status": "ok"}

    return app


app = main()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        reload=True,
        log_config=LOGGING_CONFIG
    )
