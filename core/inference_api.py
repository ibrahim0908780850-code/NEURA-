"""
NEURA-1 Hugging Face Inference Provider

Connects NEURA-1 with Hugging Face Router API.
"""

import os
import requests



class InferenceAPI:


    def __init__(self):


        self.url = (
            "https://router.huggingface.co/v1/chat/completions"
        )


        self.token = os.getenv(
            "HF_TOKEN"
        )


        self.model = os.getenv(
            "MODEL_NAME",
            "Qwen/Qwen3.5-9B"
        )


        self.system_prompt = """
You are NEURA-1.

Arabic-first advanced AI assistant.

Capabilities:
- Programming assistance
- Code analysis and debugging
- Web knowledge integration
- Reasoning
- Technical explanations

Rules:
- Reply mainly in Arabic.
- Be accurate.
- Explain clearly.
"""



    def generate(
        self,
        prompt,
        history=None,
        max_tokens=512
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
                max_tokens,


            "temperature":
                0.7,


            "top_p":
                0.9

        }



        try:


            response = requests.post(

                self.url,

                headers=headers,

                json=payload,

                timeout=60

            )



            result = response.json()



            if response.status_code != 200:

                return {

                    "error":
                        result,

                    "status_code":
                        response.status_code

                }



            if "choices" in result:


                return (
                    result["choices"][0]
                    ["message"]
                    ["content"]
                )



            return {

                "error":
                    result

            }



        except requests.exceptions.Timeout:


            return {

                "error":
                    "Request timeout"

            }



        except Exception as e:


            return {

                "error":
                    str(e)

            }




if __name__ == "__main__":


    ai = InferenceAPI()


    print(
        ai.generate(
            "مرحبا نيرا"
        )
    )