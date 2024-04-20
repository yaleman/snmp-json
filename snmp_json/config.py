from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Basic config class"""

    hostname: str = "localhost"
    community: str = "public"
    port: int = 161
    max_interfaces: int = 32
    interval: Optional[int] = None
    debug: bool = False
    timeout: int = 5
    retries: int = 0

    model_config = SettingsConfigDict(env_prefix="SNMP_JSON_")
