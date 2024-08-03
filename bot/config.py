from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: str
    openai_api_key: str


settings = Settings(_env_file=(".env.example", ".env"))
