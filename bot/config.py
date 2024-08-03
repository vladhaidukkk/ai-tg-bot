from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: str

    openai_api_key: str
    openai_proxy: str | None = None
    openai_stub_responses: bool = False

    model_config = SettingsConfigDict(env_ignore_empty=True)


settings = Settings(_env_file=(".env.example", ".env"))
