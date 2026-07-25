"""
NEURA-1 Hugging Face Inference Provider v0.9.1

Connects NEURA-1 with Hugging Face Router API.
Supports:
- Qwen/Qwen3.5-9B
- Chat completion
- History
- Error handling
"""

import os
import time
import requests


class InferenceAPI:


    def __init__(
        self,
        model_name=None
    ):

        self.name = "NEURA Inference API"


        self.url = (
            "https://router.huggingface.co/v1/chat/completions"
        )


        self.token = os.getenv(
            "HF_TOKEN"
        )


        self.model = (
            model_name
            or os.getenv(
                "MODEL_NAME",
                "Qwen/Qwen3.5-9B"
            )
        )


        self.temperature = 0.7

        self.max_tokens = 512



        self.system_prompt = """
You are NEURA-1.

Arabic-first advanced artificial intelligence system.

Your capabilities:

- Programming assistance
- Code debugging
- Reasoning
- Technical explanations
- Knowledge retrieval
- AI assistant tasks

Rules:

- Answer mainly in Arabic.
- Be accurate.
- Explain clearly.
- Do not hallucinate.
"""



    # =========================
    # Generate Response
    # =========================


    def generate(
        self,
        prompt,
        history=None,
        max_tokens=None
    ):


        if not self.token:

            return {

                "error":
                "HF_TOKEN missing"

            }



        messages = [

            {
                "role":
                "system",

                "content":
                self.system_prompt

            }

        ]



        if history:

            messages.extend(
                history
            )



        messages.append(

            {
                "role":
                "user",

                "content":
                prompt
            }

        )



        headers = {


            "Authorization":
            f"Bearer {self.token}",


            "Content-Type":
            "application/json"

        }



        payload = {


            "model":
            self.model,


            "messages":
            messages,


            "max_tokens":
            max_tokens
            or self.max_tokens,


            "temperature":
            self.temperature,


            "top_p":
            0.9

        }



        retries = 3



        for attempt in range(retries):

            try:


                response = requests.post(

                    self.url,

                    headers=headers,

                    json=payload,

                    timeout=60

                )



                data = response.json()



                if response.status_code != 200:


                    return {

                        "error":
                        data,

                        "status":
                        response.status_code,

                        "model":
                        self.model

                    }




                choices = data.get(
                    "choices"
                )



                if choices:


                    return (
                        choices[0]
                        .get("message", {})
                        .get(
                            "content",
                            ""
                        )
                    )



                return {

                    "error":
                    "Empty response"

                }




            except requests.exceptions.Timeout:


                if attempt < retries - 1:

                    time.sleep(2)

                    continue


                return {

                    "error":
                    "Request timeout"

                }



            except Exception as e:


                return {

                    "error":
                    str(e)

                }





    # =========================
    # Status
    # =========================


    def get_status(self):


        return {


            "provider":
            "Hugging Face Router",


            "model":
            self.model,


            "connected":
            bool(self.token),


            "api":
            self.url

        }





# =========================
# Test
# =========================


if __name__ == "__main__":


    ai = InferenceAPI()


    print(
        ai.get_status()
    )


    print(
        ai.generate(
            "مرحبا نيرا، عرف نفسك"
        )
    )