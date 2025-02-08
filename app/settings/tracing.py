from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, SpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

from app.settings.config import config


def setup_tracer():
    tracer = TracerProvider(
        resource=Resource.create({SERVICE_NAME: config.service_name})
    )
    trace.set_tracer_provider(tracer)
    tracer.add_span_processor(
        SimpleSpanProcessor(SpanExporter())
    )
    return tracer
