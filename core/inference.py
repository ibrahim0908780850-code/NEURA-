"""
NEURA-1 Inference Engine v1.0.0

Uses Hugging Face Inference Providers API.

Features:
- Chat Completion
- Arabic-first system prompt
- Conversation history
- Response cleaning
- Qwen compatibility
- Better error handling
"""

import os
from huggingface_hub import InferenceClient


class InferenceEngine:

    def __init__(self, model=None):

        self.model_name = (
            model
            or os.getenv(
                "MODEL_NAME",
                "Qwen/Qwen2.5-7B-Instruct"
            )
        )

        self.token = os.getenv("HF_TOKEN")

        self.client = InferenceClient(
            api_key=self.token
        )

        self.system_prompt = """
You are NEURA-1.

Arabic-first AI assistant.

Rules:
- Answer mainly in Arabic.
- Never reveal your internal reasoning.
- Return only the final answer.
- Help with programming.
- Explain clearly.
- Be concise.
"""

    # ==========================
    # Clean Response
    # ==========================

    def clean_response(self, text):

        if text is None:
            return "أعتذر، لم أتمكن من إنشاء إجابة."

        text = str(text).strip()

        if not text:
            return "أعتذر، لم أتمكن من إنشاء إجابة."

        text = text.replace("<think>", "")
        text = text.replace("</think>", "")

        if "Thinking Process:" in text:
            text = text.split("Thinking Process:")[-1]

        text = text.strip()

        return text

    # ==========================
    # Extract Response
    # ==========================

    def extract_content(self, response):

        try:

            message = response.choices[0].message

            content = getattr(message, "content", None)

            if not content:
                content = getattr(
                    message,
                    "reasoning_content",
                    None
                )

            if not content:
                content = getattr(
                    message,
                    "reasoning",
                    None
                )

            if isinstance(content, list):

                content = "".join(

                    part.get("text", "")
                    if isinstance(part, dict)
                    else str(part)

                    for part in content

                )

            return self.clean_response(content)

        except Exception:

            return "أعتذر، تعذر استخراج الرد."

    # ==========================
    # Generate
    # ==========================

    def generate(
        self,
        user_message,
        history=None,
        max_tokens=512
    ):

        if not self.token:

            return {
                "error": "HF_TOKEN missing"
            }

        messages = [
            {
                "role": "system",
                "content": self.system_prompt
            }
        ]

        if history:

            for item in history:

                if (
                    isinstance(item, dict)
                    and "role" in item
                    and "content" in item
                ):

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

                temperature=0.5,

                top_p=0.9,

                max_tokens=max_tokens

            )

            return self.extract_content(response)

        except Exception as e:

            return {
                "error": str(e),
                "model": self.model_name
            }

    # ==========================
    # Status
    # ==========================

    def status(self):

        return {
            "provider": "HuggingFace Inference",
            "model": self.model_name,
            "ready": bool(self.token)
        }


# ==========================
# Test
# ==========================

if __name__ == "__main__":

    ai = InferenceEngine()

    print(
        ai.generate("مرحباً نيرا، عرف نفسك.")
    )