help_doc = """ql add 环境变量名 环境变量值
ql cat 环境变量名
ql del 环境变量id"""
import json

import requests
from telethon import events

from .. import logger, ranran, my_chat_id, config_enum


class ql_api:
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
        res = self.s.post(url=url, data=data)
        return res

    def del_env(self, id):
        url = f"{self.url}/open/envs"
        data = json.dumps([id])
        res = self.s.delete(url=url, data=data)
        return res

    def get_env(self, env):
        url = f"{self.url}/open/envs?searchValue={env}"
        res = self.s.get(url=url).json().get("data")
        id_list = []
        value_list = []
        for i in res:
            id_list.append(i.get('id'))
            value_list.append(i.get('value'))
        return zip(id_list, value_list)


ql_config = config_enum(model_name="ql")

ranran_ql = ql_api(url=ql_config.get("ql_url"),
                   post=ql_config.get("ql_post"),
                   client_id=ql_config.get("client_id"),
                   client_secret=ql_config.get("client_secret")
                   )


@ranran.on(events.NewMessage(from_users=my_chat_id, pattern=r'ql.*'))
async def ql_env(event):
    txt = event.raw_text
    list = txt.split(' ', 2)
    common = list[1]
    if common == "cat":
        env = list[2]
        for i, j in ranran_ql.get_env(env):
            await ranran.send_message(my_chat_id, f"id={i},value={j}")
        logger.info(f"查看变量{env}")
    elif common == "add":
        list = txt.split(' ', 3)
        res = ranran_ql.add_env(new_env=list[2], value=list[3])
        await ranran.send_message(my_chat_id, f"添加变量{list[2]},{list[3]}")
        logger.info(f"添加变量{list[2]},{list[3]}")
        logger.info("结果"+res)
    elif common == "del":
        id = list[2]
        ranran_ql.del_env(id)
        await ranran.send_message(my_chat_id, f"删除变量id={id}")
        logger.info(f"删除变量id={id}")
    else:
        await ranran.send_message(my_chat_id, f"未识别的命令")
