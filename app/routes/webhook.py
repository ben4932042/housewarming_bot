import logging
from fastapi import APIRouter, Request, Response, Header, status, Depends
from linebot.exceptions import InvalidSignatureError

from app.services.line_bot import LineBotService
from app.dependencies import get_token_header

line_service = LineBotService()
logger = logging.getLogger(__name__)

route = APIRouter(
    tags=["verifications"],
    prefix="/linebot",
    dependencies=[Depends(get_token_header)],
)


@route.post("/webhook")
async def webhook_handler(request: Request, x_line_signature: str = Header(None)) -> Response:
    logger.debug("Webhook request received")
    body = await request.body()
    try:
        line_service.handler.handle(body.decode("utf-8"), x_line_signature)
    except InvalidSignatureError as e:
        logger.error(f"Invalid signature", exc_info=e)
        return Response(
            content='{"message": "invalid signature"}',
            media_type="application/json",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return Response(
        content='{"message": "ok"}',
        media_type="application/json",
        status_code=status.HTTP_200_OK
    )

