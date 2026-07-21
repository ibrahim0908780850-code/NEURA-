import os
import json


class Config:

    def __init__(self):
        self.host = os.getenv(
            "HOST",
            "0.0.0.0"
        )

        self.port = int(
            os.getenv(
                "PORT",
                8000
            )
        )

        self.model_name = "Qwen/Qwen2.5-7B-Instruct"

        self.load_config()


    def load_config(self):
        try:
            with open("config.json", "r", encoding="utf-8") as file:
                self.data = json.load(file)

        except Exception:
            self.data = {}