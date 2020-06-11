from pydantic import BaseSettings, Field


class ServiceSettings(BaseSettings):
    url_prefix: str = "/"
