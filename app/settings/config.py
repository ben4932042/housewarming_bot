import logging
import yaml
from pydantic import BaseModel, validator
from pydantic_settings import BaseSettings


class LineBot(BaseModel):
    channel_secret: str
    channel_access_token: str

    class Config:
        env_file_encoding = 'utf-8'


class GlobalConfig(BaseSettings):
    service_name: str
    log_level: str
    linebot: LineBot

    @validator("log_level")
    def validate_log_level(cls, v):
        if v.upper() not in logging.getLevelNamesMapping().keys():
            raise ValueError("Invalid log level.")
        return v

    class Config:
        env_file_encoding = 'utf-8'


def load_yaml_config(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)


yaml_config = load_yaml_config('config.yaml')
config = GlobalConfig(**yaml_config)
linebot_config = config.linebot
