"""
NEURA-1 Inference Engine

Handles text generation using the loaded Qwen model
with NEURA-1 chat template.
"""

from core.chat_template import ChatTemplate


class InferenceEngine:
    """
    Generates responses from the AI model.
    """

    def __init__(self, model=None, tokenizer=None):
        self.model = model
        self.tokenizer = tokenizer
        self.chat_template = ChatTemplate()

    def generate(self, user_message, history=None, max_tokens=256):
        """
        Generate AI response using NEURA personality.
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

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            do_sample=True,
            temperature=0.7,
            top_p=0.9
        )

        response = self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )

        # Remove prompt from generated output if included
        if prompt in response:
            response = response.replace(prompt, "").strip()

        return response


if __name__ == "__main__":

    engine = InferenceEngine()

    print(
        engine.generate(
            "مرحبا نيرا"
        )
    )