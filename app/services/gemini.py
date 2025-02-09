import re
import json
import logging
from typing import List
from pydantic import BaseModel
import google.generativeai as genai

from app.settings.prompt import PROMPT


class GeminiResponse(BaseModel):
    for_help: bool
    tags: List[str]
    reason: str
    response: str


class GeminiAPI:
    def __init__(self, api_key: str, model_name='gemini-1.5-flash'):
        self.logger = logging.getLogger(__name__)
        self.api_key = api_key
        self.model_name = model_name
        self.client = self._init_genai_client()

    def _init_genai_client(self):
        genai.configure(api_key=self.api_key)
        return genai.GenerativeModel(self.model_name)

    def call_api(self, text: str):
        return self.client.generate_content(PROMPT + text)

    def response(self, text: str) -> GeminiResponse:
        response = self.call_api(text)
        return GeminiResponse(**try_parse_json(response.text))


def try_parse_json(json_str: str) -> dict:
    try:
        return json.loads(json_str)
    except json.decoder.JSONDecodeError:
        json_str = re.sub(r"```json\n|\n```", "", json_str)
        return json.loads(json_str)
