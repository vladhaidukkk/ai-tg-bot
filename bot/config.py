from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: str


settings = Settings(_env_file=(".env.example", ".env"))
