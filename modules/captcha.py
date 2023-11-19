import requests
from modules import logging
import time

logger = logging.Logger()


class HCoptcha:
    def __init__(self, key: str):
        self.key = key

    def _createTask(self, proxy: str) -> str:
        try:
            response = requests.post(
                "https://api.hcoptcha.online/api/createTask",
                json={
                    "task_type": "hcaptchaEnterprise",
                    "api_key": self.key,
                    "data": {
                        "sitekey": "f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34",
                        "url": "https://discord.com/login",
                        "proxy": proxy,
                    },
                },
            )
            return response.json()["task_id"]
        except Exception as error:
            logger._error(error)

    def _getResult(self, task_id: str) -> str:
        response = requests.post(
            "https://api.hcoptcha.online/api/getTaskData",
            json={"api_key": self.key, "task_id": task_id},
        )
        while response.json()["task"]["state"] != "completed":
            resp = requests.post(
                "https://api.hcoptcha.online/api/getTaskData",
                json={"api_key": self.key, "task_id": task_id},
            )
            if resp.json()["task"]["state"] == "completed":
                return resp.json()["task"]["captcha_key"]
            else:
                time.sleep(3)
                pass
