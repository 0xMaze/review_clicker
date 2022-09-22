import io
from datetime import datetime
import requests as req
from configparser import ConfigParser


class KeyManager:
    def __init__(self):
        self.cfg = ConfigParser()
        self.cfg.read("config.ini")
        self.key = ""
        self.url = f"http://127.0.0.1:5000/api/keys/{self.key}"
        self.key_full_data = {}

    def set_key(self, key):
        self.key = key

    def key_exists(self):
        response = req.get(self.url)

        if response.json() == {}:
            return False

        self.remember_key(key=self.key)
        return True

    def validate_key(self):
        self.cfg.read("config.ini")
        if not self.cfg.has_option("Key", "key") or not self.cfg.has_option(
            "Key", "end_date"
        ):
            return False

        # Wed, 09 Oct 2024 00:00:00 GMT

        date = datetime.strptime(
            self.cfg["Key"]["end_date"], "%a, %d %b %Y %H:%M:%S %Z"
        )

        if date < datetime.now() or not self.key_exists():
            return False

        return True

    def reset_key(self):
        self.cfg.remove_option("Key", "key")
        self.cfg["Key"]["is_activated"] = "false"
        self.cfg.remove_option("Key", "end_date")

        with io.open("config.ini", "w") as configfile:
            self.cfg.write(configfile)

    def key_outdated(self):
        date = datetime.strptime(
            self.cfg["Key"]["end_date"], "%a, %d %b %Y %H:%M:%S %Z"
        )

        if date < datetime.now():
            return False
        else:
            return True

    def remember_key(self, key):
        self.cfg["Key"]["key"] = key
        self.cfg["Key"]["is_activated"] = "true"
        self.cfg["Key"]["end_date"] = req.get(self.url, json={"key": key}).json()[
            "end_date"
        ]

        with io.open("config.ini", "w") as configfile:
            self.cfg.write(configfile)

    def key_is_activated(self):
        if self.cfg["Key"]["is_activated"] == "true":
            return True
        else:
            return False
