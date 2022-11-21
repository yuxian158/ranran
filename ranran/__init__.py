import importlib.util
import json
import logging
import os
import sys

import tomli as tomli
from telethon import TelegramClient
from telethon.sessions import StringSession


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
    def __init__(self, model_name, toml_path="data/config/config.toml"):
        self.toml_path = toml_path
        self.model_name = model_name

    def get(self, key):
        with open(self.toml_path, "rb") as f:
            toml_dict = tomli.load(f).get(self.model_name)
            return toml_dict.get(key)


logging.basicConfig(
    format='%(asctime)s-%(name)s-%(levelname)s=> [%(funcName)s] %(message)s ', level=logging.INFO, filename="bot.log",
    filemode='w', encoding="utf8")
logger = logging.getLogger(__name__)

ranran_config_path = os.getenv('ranran_config_path', 'null')
if ranran_config_path == 'null':
    ranran_config = config_enum("ranran")
else:
    ranran_config = config_enum("ranran", "ranran_config_path")
logger.info(f"配置文件路径为{ranran_config.toml_path}")

API_ID = ranran_config.get("API_ID")
API_HASH = ranran_config.get("API_HASH")
TOKEN = ranran_config.get("TOKEN")
my_chat_id = ranran_config.get("my_chat_id")
session = ranran_config.get("session")

if session is None:
    with TelegramClient(StringSession(), API_ID, API_HASH) as client:
        logger.info("请将以下内容填入config.toml")
        print(client.session.save())
else:
    logger.info("正在启动然然")
    ranran = TelegramClient(StringSession(session), API_ID, API_HASH).start(bot_token=TOKEN)

# logger.info("正在启用青龙管理插件")
#
# logger.info("加载帮助中")

logger.info('加载插件中...')
load_module('plugin', "ranran/plugin/")
