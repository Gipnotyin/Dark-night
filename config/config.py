from dataclasses import dataclass

from environs import Env

@dataclass
class Database:
    host: str
    port: int
    user: str
    password: str
    database: str

@dataclass
class TgBot:
    token: str
    id_admin: list[int]

@dataclass
class Config:
    database: Database
    tg_bot: TgBot

def load_config(path: str | None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        database=Database(
            host=env('HOST'),
            port=env('PORT'),
            user=env('USER'),
            password=env('PASSWORD'),
            database=env('DATABASE')
        ),
        tg_bot=TgBot(
            token=env('TOKEN'),
            id_admin=list(map(int, env.list('ID_ADMIN')))
        )
    )