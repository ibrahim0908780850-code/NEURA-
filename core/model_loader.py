"""
NEURA-1 Model Loader

Responsible for loading and managing
the base AI model.
"""

from transformers import AutoTokenizer, AutoModelForCausalLM

from core.config import Config


class ModelLoader:
    """
    Loads the foundation model for NEURA-1.
    """

    def __init__(self, model_name=None):

        self.config = Config()

        self.model_name = (
            model_name
            or self.config.model_name
        )

        self.tokenizer = None
        self.model = None


    def load(self):
        """
        Load tokenizer and model.
        """

        print(
            f"Loading model: {self.model_name}"
        )

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name
        )

        return self.model


    def get_status(self):
        """
        Return model status.
        """

        return {
            "model": self.model_name,
            "loaded": self.model is not None
        }


if __name__ == "__main__":

    loader = ModelLoader()

    loader.load()

    print(
        loader.get_status()
    )