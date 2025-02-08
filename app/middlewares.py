from typing import Callable
import json
import logging

from fastapi import FastAPI, Request
from fastapi.middleware import Middleware
from opentelemetry import trace
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.types import Message


class TraceIdMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next) -> Response:
        trace_id = format(trace.get_current_span().get_span_context().trace_id, '032x')
        request.state.trace_id = trace_id
        response = await call_next(request)
        response.headers["X-Trace-ID"] = trace_id
        return response


class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, *, logger: logging.Logger) -> None:
        self._logger = logger
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:

        await self.set_body(request)
        logging_dict = dict()

        response, response_dict = await self._log_response(call_next, request)
        request_dict = await self._log_request(request)
        logging_dict["request"] = request_dict
        logging_dict["response"] = response_dict
        logging_dict["trace_id"] = response.headers.get("X-Trace-ID", "")

        self._logger.info(logging_dict)

        return response

    async def set_body(self, request: Request) -> None:
        """Avails the response body to be logged within a middleware as,
            it is generally not a standard practice.

               Arguments:
               - request: Request
               Returns:
               - receive_: Receive
        """
        receive_ = await request._receive()

        async def receive() -> Message:
            return receive_

        request._receive = receive

    async def _log_request(self, request: Request) -> dict:

        path = request.url.path
        if request.query_params:
            path += f"?{request.query_params}"

        request_logging = {
            "method": request.method,
            "path": path,
            "ip": request.client.host
        }

        try:
            request_logging["body"] = await request.json()
        except Exception:
            request_logging["body"] = None

        return request_logging

    async def _log_response(self, call_next: Callable, request: Request) -> tuple[Response, dict]:

        response = await self._execute_request(call_next, request)
        response_logging = {
            "status_code": response.status_code,
        }

        resp_body = [section async for section in response.__dict__["body_iterator"]]
        response.__setattr__("body_iterator", AsyncIteratorWrapper(resp_body))

        try:
            resp_body = json.loads(resp_body[0].decode())
        except:
            resp_body = str(resp_body)

        response_logging["body"] = resp_body

        return response, response_logging

    async def _execute_request(self, call_next: Callable, request: Request) -> Response:
        try:
            response: Response = await call_next(request)
            return response

        except Exception as e:
            self._logger.exception(
                {
                    "path": request.url.path,
                    "method": request.method,
                    "reason": e
                }
            )


class AsyncIteratorWrapper:
    def __init__(self, obj):
        self._it = iter(obj)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            value = next(self._it)
        except StopIteration:
            raise StopAsyncIteration
        return value
