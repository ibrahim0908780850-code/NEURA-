"""
NEURA-1 Hugging Face Inference API v0.9.3

Connects NEURA-1 with Hugging Face Router API.

Features:
- Chat Completions
- Arabic-first AI prompt
- History support
- Response cleaning
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


        self.temperature = 0.5

        self.max_tokens = 512



        self.system_prompt = """

You are NEURA-1.

Arabic-first advanced AI assistant.


Capabilities:

- Arabic conversation
- Programming assistance
- Code debugging
- Technical explanations
- Knowledge retrieval
- Problem solving


Rules:

- Answer mainly in Arabic.
- Be accurate.
- Explain clearly.
- Never reveal internal reasoning.
- Return only the final answer.

"""





    # =========================
    # Clean Response
    # =========================


    def clean_response(
        self,
        content
    ):


        if not content:

            return (
                "أعتذر، لم يتم إنشاء رد."
            )



        content = str(
            content
        ).strip()



        # Remove reasoning leakage

        if "Thinking Process:" in content:

            content = content.split(
                "Thinking Process:"
            )[0].strip()



        if "reasoning" in content.lower():

            return (
                "أعتذر، حدث خطأ "
                "في معالجة الإجابة."
            )



        return content






    # =========================
    # Generate
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





        # Add history safely

        if history:


            for item in history:


                if (

                    isinstance(
                        item,
                        dict
                    )

                    and

                    "role" in item

                    and

                    "content" in item

                ):


                    messages.append({

                        "role":
                        item["role"],

                        "content":
                        item["content"]

                    })





        messages.append({

            "role":
            "user",

            "content":
            prompt

        })





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
            max_tokens or self.max_tokens,


            "temperature":
            self.temperature,


            "top_p":
            0.9


        }





        for attempt in range(3):


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
                    "choices",
                    []
                )




                if not choices:


                    return {

                        "error":
                        "No response choices",

                        "raw":
                        data

                    }






                message = choices[0].get(
                    "message",
                    {}
                )



                content = message.get(
                    "content",
                    ""
                )



                return self.clean_response(
                    content
                )






            except requests.exceptions.Timeout:



                if attempt < 2:


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


    def get_status(
        self
    ):


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