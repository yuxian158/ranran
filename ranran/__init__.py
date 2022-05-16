import json
import logging

import requests as requests
import tomli as tomli
from telethon import TelegramClient
from telethon.sessions import StringSession


class config_enum:
    def __init__(self, toml_path="config.toml"):
        self.toml_path = toml_path

    def ranran_get(self, key):
        with open(self.toml_path, "rb") as f:
            toml_dict = tomli.load(f).get("ranran")
            return toml_dict.get(key)

    def ql_get(self, key):
        with open(self.toml_path, "rb") as f:
            toml_dict = tomli.load(f).get("ql")
            return toml_dict.get(key)


class ql:
    def __init__(self, url, post, client_id, client_secret):
        self.url = f"http://{url}:{post}"
        self.client_id = client_id
        self.client_secret = client_secret
        self.s = requests.session()
        self._get_qltoken()

    def _get_qltoken(self):
        url = f"{self.url}/open/auth/token?client_id={self.client_id}&client_secret={self.client_secret}"
        res = self.s.get(url)
        token = json.loads(res.text)["data"]['token']
        self.s.headers.update({"authorization": "Bearer " + str(token)})
        self.s.headers.update({"Content-Type": "application/json;charset=UTF-8"})

    def add_env(self, new_env, value):
        url = f"{self.url}/open/envs"
        data = [{"value": value, "name": new_env}]
        data = json.dumps(data)
        print(self.s.post(url=url, data=data))


logging.basicConfig(
    format='%(asctime)s-%(name)s-%(levelname)s=> [%(funcName)s] %(message)s ', level=logging.INFO, filename="bot.log",
    filemode='w', encoding="utf8")
logger = logging.getLogger(__name__)

cf = config_enum()
API_ID = cf.ranran_get("API_ID")
API_HASH = cf.ranran_get("API_HASH")
TOKEN = cf.ranran_get("TOKEN")
my_chat_id = cf.ranran_get("my_chat_id")
session = cf.ranran_get("session")
download_path = cf.ranran_get("download_path")
host = cf.ranran_get("host")

if session is None:
    with TelegramClient(StringSession(), API_ID, API_HASH) as client:
        logger.info("请将以下内容填入config.toml")
        print(client.session.save())
else:
    ranran = TelegramClient(StringSession(session), API_ID, API_HASH).start(bot_token=TOKEN)

ranran_ql = ql(url=cf.ql_get("ql_url"),
        post=cf.ql_get("ql_post"),
        client_id=cf.ql_get("client_id"),
        client_secret=cf.ql_get("client_secret"))
