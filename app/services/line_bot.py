from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage

from app.settings.config import linebot_config as config


class LineBotService:
    def __init__(self) -> None:
        self.line_bot_api = LineBotApi(config.channel_access_token)
        self.handler = WebhookHandler(config.channel_secret)
        self._setup_handler()

    def _setup_handler(self) -> None:
        @self.handler.add(MessageEvent, message=TextMessage)
        def handle_message(event: MessageEvent):
            self.echo(event)

    def echo(self, event: MessageEvent) -> None:
        # self.line_bot_api.reply_message(
        #     event.reply_token,
        #     TextSendMessage(text=event.message.text)
        # )
        return None
