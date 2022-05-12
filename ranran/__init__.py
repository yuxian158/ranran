import logging

import tomli as tomli
from telethon import TelegramClient


class config_enum():
    def __init__(self, toml_path="config.toml"):
        self.toml_path = toml_path

    def get(self, key):
        with open(self.toml_path, "rb") as f:
            toml_dict = tomli.load(f).get("ranran")
            return toml_dict.get(key)


logging.basicConfig(
    format='%(asctime)s-%(name)s-%(levelname)s=> [%(funcName)s] %(message)s ', level=logging.INFO, filename="bot.log",
    filemode='w',encoding="utf8")
logger = logging.getLogger(__name__)

cf = config_enum()
API_ID = cf.get("API_ID")
API_HASH = cf.get("API_HASH")
TOKEN = cf.get("TOKEN")
my_chat_id = cf.get("my_chat_id")
session = cf.get("session")
download_path = cf.get("download_path")

ranran = TelegramClient('ranran', API_ID, API_HASH).start(bot_token=TOKEN)
