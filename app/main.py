import logging
from fastapi import status, FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from app.middlewares import TraceIdMiddleware, LoggingMiddleware
from app.routes.webhook import route as webhook_route
from app.routes.healthcheck import route as healthcheck_route
from app.settings.logging import LOGGING_CONFIG, setup_logger
from app.settings.tracing import setup_tracer
from app.settings.config import config


def main() -> FastAPI:

    middleware = [
        Middleware(LoggingMiddleware, logger=setup_logger()),
        Middleware(TraceIdMiddleware),
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
            allow_credentials=True,
        )
    ]

    app = FastAPI(
        title=config.service_name,
        middleware=middleware,
        redoc_url=None
    )

    FastAPIInstrumentor.instrument_app(app, tracer_provider=setup_tracer())
    app.include_router(
        router=webhook_route,
        prefix="/api/v1"
    )
    app.include_router(
        router=healthcheck_route,
    )

    return app


app = main()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        reload=True,
        log_config=LOGGING_CONFIG
    )
