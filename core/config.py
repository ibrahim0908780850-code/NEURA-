import os
import json


class Config:

    def __init__(self):

        # System information
        self.app_name = "NEURA-1"
        self.version = "0.5.0"
        self.organization = "Neural AI Organization"
        self.description = "Arabic-first intelligent AI system"

        # Server settings
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

        # Model settings
        self.model_name = "Qwen/Qwen2.5-7B-Instruct"

        self.temperature = 0.7
        self.max_tokens = 256

        # Language
        self.primary_language = "ar"
        self.supported_languages = [
            "ar",
            "en"
        ]

        # Load JSON config
        self.load_config()


    def load_config(self):

        try:
            with open(
                "config.json",
                "r",
                encoding="utf-8"
            ) as file:

                self.data = json.load(file)

        except Exception:

            self.data = {}