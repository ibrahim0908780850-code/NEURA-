"""
NEURA-1 Model Loader v0.9

Connects NEURA-1 with external AI inference providers.
"""

from core.config import Config
from core.inference_api import InferenceAPI


class ModelLoader:
    """
    Loads and manages the AI model connection.
    """


    def __init__(
        self,
        model_name=None
    ):

        self.config = Config()


        self.model_name = (

            model_name

            or getattr(
                self.config,
                "model_name",
                "Qwen/Qwen3.5-9B"
            )

        )


        self.model = None


        self.inference = InferenceAPI(
            model_name=self.model_name
        )



    # =========================
    # Load Model
    # =========================

    def load(self):

        """
        Initialize external inference connection.
        """


        if self.model:

            return self.model



        print(
            f"Connecting model: {self.model_name}"
        )


        try:

            self.model = self.inference

            return self.model



        except Exception as e:


            print(
                "Model connection failed:",
                str(e)
            )


            self.model = None


            raise e




    # =========================
    # Generate
    # =========================

    def generate(
        self,
        prompt
    ):

        """
        Generate AI response.
        """


        if self.model is None:

            self.load()



        return self.model.generate(
            prompt
        )




    # =========================
    # Status
    # =========================

    def get_status(
        self
    ):

        """
        Return model status.
        """


        return {


            "model":

            self.model_name,


            "loaded":

            self.model is not None,


            "provider":

            "Hugging Face / OpenRouter"



        }




# =========================
# Test
# =========================

if __name__ == "__main__":


    loader = ModelLoader()


    loader.load()


    print(
        loader.get_status()
    )