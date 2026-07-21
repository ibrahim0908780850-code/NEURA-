"""
NEURA-1 Inference Engine

Handles text generation using the loaded Qwen model.
"""


class InferenceEngine:
    """
    Generates responses from the AI model.
    """

    def __init__(self, model=None, tokenizer=None):
        self.model = model
        self.tokenizer = tokenizer

    def generate(self, prompt, max_tokens=256):
        """
        Generate AI response.
        """

        if self.model is None or self.tokenizer is None:
            return "NEURA-1 model is not loaded yet."

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt"
        )

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_tokens
        )

        response = self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )

        return response


if __name__ == "__main__":

    engine = InferenceEngine()

    print(
        engine.generate(
            "مرحبا نيرا"
        )
    )