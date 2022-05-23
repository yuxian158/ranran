import json

import requests

from ranran import logger


class ql_api:
    def __init__(self, url, post, client_id, client_secret, logger):
        self.url = f"http://{url}:{post}"
        self.client_id = client_id
        self.client_secret = client_secret
        self.s = requests.session()
        self.logger = logger
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
        self.logger.info(res)

    def del_env(self, id):
        url = f"{self.url}/open/envs"
        data = json.dumps([id])
        res = self.s.delete(url=url, data=data)
        self.logger.info(res)

    def get_env(self, env):
        url = f"{self.url}/open/envs?searchValue={env}"
        res = self.s.get(url=url).json().get("data")
        id_list = []
        value_list = []
        for i in res:
            id_list.append(i.get('id'))
            value_list.append(i.get('value'))
        return zip(id_list, value_list)
