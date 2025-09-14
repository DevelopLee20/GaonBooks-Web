from pydantic_settings import BaseSettings


class Env(BaseSettings):
    DB_URI: str
    MODE: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"


env = Env()  # type: ignore
