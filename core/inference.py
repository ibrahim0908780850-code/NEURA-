"""
NEURA-1 Inference Engine

Uses Hugging Face Inference Providers API.
"""

import os

from huggingface_hub import InferenceClient



class InferenceEngine:


    def __init__(
        self,
        model=None,
        tokenizer=None
    ):


        self.model_name = (
            model
            or os.getenv(
                "MODEL_NAME",
                "Qwen/Qwen3.5-9B"
            )
        )


        self.client = InferenceClient(

            api_key=os.getenv(
                "HF_TOKEN"
            )

        )


        self.system_prompt = """
You are NEURA-1.

Arabic-first advanced AI assistant.

Rules:
- Answer mainly in Arabic.
- Help with programming and debugging.
- Explain concepts clearly.
- Use tools when available.
- Be accurate and concise.
"""



    def generate(
        self,
        user_message,
        history=None,
        max_tokens=512
    ):


        if not os.getenv("HF_TOKEN"):

            return {
                "error":
                    "HF_TOKEN missing"
            }



        messages = [


            {
                "role": "system",
                "content":
                    self.system_prompt
            }

        ]



        if history:


            for item in history:


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
                user_message

        })



        try:


            response = (
                self.client
                .chat.completions
                .create(

                    model=self.model_name,

                    messages=messages,

                    max_tokens=max_tokens,

                    temperature=0.7,

                    top_p=0.9

                )
            )



            return (
                response
                .choices[0]
                .message
                .content
            )



        except Exception as e:


            return {

                "error":
                    str(e),

                "model":
                    self.model_name

            }




if __name__ == "__main__":


    ai = InferenceEngine()


    print(
        ai.generate(
            "مرحبا نيرا"
        )
    )