"""
NEURA-1 Inference Engine

Uses Hugging Face Inference Providers API.
"""

import os
from huggingface_hub import InferenceClient


class InferenceEngine:

    def __init__(self, model=None, tokenizer=None):

        self.model_name = (
            model
            or os.getenv(
                "MODEL_NAME",
                "Qwen/Qwen2.5-7B-Instruct:fastest
            )
        )

        self.client = InferenceClient(
            api_key=os.getenv(
                "HF_TOKEN"
            )
        )


    def generate(
        self,
        user_message,
        history=None,
        max_tokens=256
    ):

        messages = []


        if history:

            for item in history:

                messages.append({
                    "role": item["role"],
                    "content": item["content"]
                })


        messages.append({
            "role": "user",
            "content": user_message
        })


        try:

            response = self.client.chat.completions.create(

                model=self.model_name,

                messages=messages,

                max_tokens=max_tokens,

                temperature=0.7

            )


            return (
                response
                .choices[0]
                .message
                .content
            )


        except Exception as e:

            return {
                "error": str(e)
            }