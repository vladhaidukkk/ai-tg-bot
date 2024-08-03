from pydantic import BaseModel, Field, PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BotSettings(BaseModel):
    token: str


class OpenAISettings(BaseModel):
    api_key: str
    proxy: str | None = None
    stub_responses: bool = False


class DatabaseSettings(BaseModel):
    username: str
    password: str | None = None
    host: str
    port: int = Field(ge=1, le=65535)
    name: str

    @computed_field
    @property
    def url(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            path=self.name,
        )


class AlchemySettings(BaseModel):
    echo: bool = False
    echo_pool: bool = False
    max_overflow: int = 10


class Settings(BaseSettings):
    bot: BotSettings
    openai: OpenAISettings
    db: DatabaseSettings
    alchemy: AlchemySettings = AlchemySettings()

    model_config = SettingsConfigDict(env_nested_delimiter="__", env_ignore_empty=True)


settings = Settings(_env_file=(".env.example", ".env"))
