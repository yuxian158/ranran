import importlib.util
import json
import logging
import os
import sys

import requests as requests
import tomli as tomli
from telethon import TelegramClient
from telethon.sessions import StringSession
from .tools import ql_api


def load_module(module, path):
    files = os.listdir(path)
    for file in files:
        try:
            if file.endswith('.py'):
                filename = file.replace('.py', '')
                name = "ranran.{}.{}".format(module, filename)
                spec = importlib.util.spec_from_file_location(name, path + file)
                load = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(load)
                sys.modules[f"ranran.{module}.{filename}"] = load
                logger.info(f"然然加载-->{filename}-->完成")
        except Exception as e:
            logger.info(f"ranran加载失败-->{file}-->{str(e)}")
            continue


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
    logger.info("正在启动然然")
    ranran = TelegramClient(StringSession(session), API_ID, API_HASH).start(bot_token=TOKEN)

logger.info("正在启用青龙管理插件")
ranran_ql = ql_api(url=cf.ql_get("ql_url"),
                   post=cf.ql_get("ql_post"),
                   client_id=cf.ql_get("client_id"),
                   client_secret=cf.ql_get("client_secret"),
                   logger=logger)

logger.info("加载帮助中")

logger.info('加载插件中...')
load_module('plugin', "ranran/plugin/")
