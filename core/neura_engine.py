"""
NEURA-1 Core Engine

Connects NEURA intelligence with the Qwen model
and inference system.
"""

from datetime import datetime

from core.model_loader import ModelLoader
from core.inference import InferenceEngine


class NEURAEngine:
    """
    Main AI engine for NEURA-1.
    """

    def __init__(self):
        self.name = "NEURA-1"
        self.version = "0.3.0"

        self.model_loader = ModelLoader()

        self.model = None
        self.inference = None

        self.created = datetime.utcnow()

    def load_model(self):
        """
        Load Qwen model and initialize inference.
        """

        self.model = self.model_loader.load()

        self.inference = InferenceEngine(
            model=self.model,
            tokenizer=self.model_loader.tokenizer
        )

        return {
            "status": "model loaded",
            "model": self.model_loader.model_name
        }

    def process_message(self, message, user_id=None):
        """
        Process user message and generate response.
        """

        if self.inference is None:
            return {
                "response": "NEURA-1 model is not loaded yet.",
                "user_id": user_id,
                "status": "waiting"
            }

        response = self.inference.generate(
            message
        )

        return {
            "response": response,
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat()
        }

    def get_status(self):
        """
        Return system status.
        """

        return {
            "name": self.name,
            "version": self.version,
            "model_loaded": self.model is not None,
            "inference_ready": self.inference is not None
        }