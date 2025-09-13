from pydantic_settings import BaseSettings


class Env(BaseSettings):
    DB_URI: str
    MODE: str

    class Config:
        env_file = ".env"


env = Env() # type: ignore
