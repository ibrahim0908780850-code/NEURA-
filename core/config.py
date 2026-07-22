import os
import json


class Config:

    def __init__(self):

        # System information
        self.app_name = os.getenv("APP_NAME", "NEURA-1")
        self.version = os.getenv("APP_VERSION", "0.5.0")
        self.organization = "Neural AI Organization"
        self.description = "Arabic-first intelligent AI system"

        # Server
        self.host = os.getenv("HOST", "0.0.0.0")
        self.port = int(os.getenv("PORT", 8000))

        # Model
        self.model_name = os.getenv(
            "MODEL_NAME",
            "Qwen/Qwen3.5-9B"
        )

        self.temperature = float(
            os.getenv("TEMPERATURE", 0.7)
        )

        self.max_tokens = int(
            os.getenv("MAX_TOKENS", 256)
        )

        # Languages
        self.primary_language = "ar"
        self.supported_languages = [
            "ar",
            "en"
        ]

        self.load_config()


    def load_config(self):

        try:
            with open(
                "config.json",
                "r",
                encoding="utf-8"
            ) as f:

                self.data = json.load(f)

        except Exception:

            self.data = {}