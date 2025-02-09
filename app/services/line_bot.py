import logging

from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from app.services.gemini import GeminiAPI
from app.settings.config import config


class LineBotService:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.llm = GeminiAPI(config.gemini_api_key)
        self.line_bot_api = LineBotApi(config.linebot.channel_access_token)
        self.handler = WebhookHandler(config.linebot.channel_secret)
        self._setup_handler()

    def _setup_handler(self) -> None:
        @self.handler.add(MessageEvent, message=TextMessage)
        def handle_message(event: MessageEvent):
            try:
                self.handle_event(event)
            except Exception as e:
                self.logger.error("Error occurred", exc_info=e)

    def handle_event(self, event: MessageEvent) -> None:

        self.logger.info({"input_text": f"{event.message.text}"})
        input_text = event.message.text

        output = self.llm.response(input_text)
        self.logger.info({"output": output})

        self.line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"{output.response}")
        )
