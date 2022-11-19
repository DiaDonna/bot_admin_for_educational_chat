from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    token: str
    send_report_to_owner: bool


@dataclass
class Miscellaneous:
    hastebin_url: str
    verified_groups: list[int]


@dataclass
class Config:
    tg_bot: TgBot
    misc: Miscellaneous


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            send_report_to_owner=env.bool("SEND_REPORT_TO_OWNER"),
        ),
        misc=Miscellaneous(
            hastebin_url=env.str("HASTEBIN_URL"),
            verified_groups=list(map(int, env.list("VERIFIED_GROUPS")))
        )
    )
