"""
NEURA-1 Model Loader v0.9.2

Connects NEURA-1 with external AI inference providers.

Features:
- Model connection management
- Safe response parsing
- Empty content protection
"""

from core.config import Config
from core.inference_api import InferenceAPI



class ModelLoader:
    """
    Loads and manages AI model connection.
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


        self.status = "initialized"



    # =========================
    # Load Model
    # =========================

    def load(self):

        if self.model is not None:

            return self.model



        print(
            f"🧠 Connecting model: {self.model_name}"
        )


        try:

            self.model = self.inference

            self.status = "connected"


            return self.model



        except Exception as e:


            self.status = "failed"


            raise RuntimeError(
                f"Model loading failed: {str(e)}"
            )



    # =========================
    # Safe Generate
    # =========================

    def generate(
        self,
        prompt,
        history=None,
        max_tokens=512
    ):


        if self.model is None:

            self.load()



        try:


            result = self.model.generate(

                prompt,

                history=history,

                max_tokens=max_tokens

            )



            return self.parse_response(
                result
            )



        except Exception as e:


            return {

                "response":
                "حدث خطأ أثناء توليد الرد",

                "error":
                str(e)

            }



    # =========================
    # Response Parser
    # =========================

    def parse_response(
        self,
        result
    ):


        # نص مباشر

        if isinstance(result, str):

            return result



        # JSON Response

        if isinstance(result, dict):


            # OpenAI compatible

            choices = result.get(
                "choices"
            )


            if choices:


                message = choices[0].get(
                    "message",
                    {}
                )


                content = message.get(
                    "content"
                )


                if content and content.strip():

                    return content



                # حماية من كشف reasoning

                return (
                    "أهلاً بك! "
                    "أنا NEURA-1، "
                    "كيف يمكنني مساعدتك؟"
                )



            # Provider response

            if result.get("response"):

                return result["response"]



        return str(result)



    # =========================
    # Reload
    # =========================

    def reload(self):

        self.model = None

        self.status = "reloading"


        return self.load()



    # =========================
    # Status
    # =========================

    def get_status(self):

        return {

            "model":
            self.model_name,


            "loaded":
            self.model is not None,


            "provider":
            "Hugging Face Router API",


            "status":
            self.status

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