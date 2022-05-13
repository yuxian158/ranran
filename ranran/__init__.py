import logging
import tomli as tomli
from telethon import TelegramClient
from telethon.sessions import StringSession


class config_enum():
    def __init__(self, toml_path="config.toml"):
        self.toml_path = toml_path

    def get(self, key):
        with open(self.toml_path, "rb") as f:
            toml_dict = tomli.load(f).get("ranran")
            return toml_dict.get(key)


logging.basicConfig(
    format='%(asctime)s-%(name)s-%(levelname)s=> [%(funcName)s] %(message)s ', level=logging.INFO, filename="bot.log",
    filemode='w', encoding="utf8")
logger = logging.getLogger(__name__)

cf = config_enum()
API_ID = cf.get("API_ID")
API_HASH = cf.get("API_HASH")
TOKEN = cf.get("TOKEN")
my_chat_id = cf.get("my_chat_id")
session = cf.get("session")
download_path = cf.get("download_path")
host = cf.get("host")
if session is None:
    with TelegramClient(StringSession(), API_ID, API_HASH) as client:
        logger.info("请将以下内容填入config.toml")
        print(client.session.save())
else:
    ranran = TelegramClient(StringSession(session), API_ID, API_HASH).start(bot_token=TOKEN)
