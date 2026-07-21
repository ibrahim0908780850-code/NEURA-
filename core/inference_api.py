"""
NEURA-1 Inference API

Connects NEURA-1 with external AI model providers.
"""

import os
import requests


class InferenceAPI:
    """
    Handles communication with AI inference endpoint.
    """

    def __init__(self):

        self.url = os.getenv(
            "MODEL_API_URL"
        )

        self.token = os.getenv(
            "HF_TOKEN"
        )


    def generate(self, prompt):
        """
        Send prompt to AI model and return response.
        """

        if not self.url:
            return {
                "error": "MODEL_API_URL is not configured"
            }


        headers = {}

        if self.token:
            headers["Authorization"] = (
                f"Bearer {self.token}"
            )


        try:

            response = requests.post(
                self.url,
                headers=headers,
                json={
                    "inputs": prompt,
                    "parameters": {
                        "max_new_tokens": 256,
                        "temperature": 0.7
                    }
                },
                timeout=60
            )


            result = response.json()


            if isinstance(result, list):

                return result[0].get(
                    "generated_text",
                    ""
                )


            return result


        except Exception as error:

            return {
                "error": str(error)
            }