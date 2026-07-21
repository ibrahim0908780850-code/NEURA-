"""
NEURA-1 Inference Engine

Handles text generation using the loaded Qwen model
with NEURA-1 chat template.
"""

import torch

from core.chat_template import ChatTemplate


class InferenceEngine:
    """
    Generates responses from NEURA-1 model.
    """

    def __init__(self, model=None, tokenizer=None):

        self.model = model
        self.tokenizer = tokenizer

        self.chat_template = ChatTemplate()


    def generate(
        self,
        user_message,
        history=None,
        max_tokens=256
    ):
        """
        Generate AI response.
        """

        if self.model is None or self.tokenizer is None:
            return "NEURA-1 model is not loaded yet."


        prompt = self.chat_template.format_prompt(
            user_message,
            history
        )


        inputs = self.tokenizer(
            prompt,
            return_tensors="pt"
        )


        if torch.cuda.is_available():
            inputs = {
                key: value.to("cuda")
                for key, value in inputs.items()
            }


        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.1
        )


        response = self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )


        if prompt in response:
            response = response.replace(
                prompt,
                ""
            )


        return response.strip()


if __name__ == "__main__":

    engine = InferenceEngine()

    print(
        engine.generate(
            "مرحبا نيرا"
        )
    )