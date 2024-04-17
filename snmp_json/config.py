from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Basic config class"""

    hostname: str = "localhost"
    community: str = "public"
    port: int = 161
    max_interfaces: int = 32

    model_config = SettingsConfigDict(env_prefix="SNMP_JSON_")
