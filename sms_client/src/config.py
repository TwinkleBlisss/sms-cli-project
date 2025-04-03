import os
import re
import tomllib
from pydantic import BaseModel, SecretStr, field_validator

class Config(BaseModel):
    url: str
    username: str
    password: SecretStr

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: str) -> str | Exception:
        pattern = r"^http://[a-zA-Z0-9.-]+:\d+/send_sms$"
        if not re.match(pattern, value):
            raise ValueError("Invalid URL format. Expected format: http://host:port/send_sms")
        return value


class AppConfig(BaseModel):
    api: Config


def load_config(path: str = r"sms_client\config.toml") -> AppConfig:
    with open(path, "rb") as f:
        config_data = tomllib.load(f)
        return AppConfig(**config_data)


if "src" in os.getcwd():
    config = load_config(path=r"..\config.toml")
else:
    config = load_config()
