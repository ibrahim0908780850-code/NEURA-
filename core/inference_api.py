"""
NEURA-1 Hugging Face Inference Provider
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


    def generate(self, prompt):

        if not self.token:
            return {
                "error": "HF_TOKEN missing"
            }


        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }


        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 256,
            "temperature": 0.7
        }


        try:

            response = requests.post(
                self.url,
                headers=headers,
                json=data,
                timeout=60
            )


            result = response.json()


            if "choices" in result:

                return (
                    result["choices"][0]
                    ["message"]
                    ["content"]
                )


            return {
                "error": result
            }


        except Exception as e:

            return {
                "error": str(e)
            }