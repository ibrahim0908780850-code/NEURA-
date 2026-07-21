"""
NEURA-1 Chat Template

Defines system instructions and conversation format.
"""


class ChatTemplate:
    """
    Formats conversations for NEURA-1.
    """

    def __init__(self):

        self.system_prompt = """
You are NEURA-1, an advanced Arabic-first AI assistant.

Core abilities:
- Understand Arabic and English.
- Help with programming, learning, and daily tasks.
- Provide accurate and useful answers.
- Use memory, knowledge, and tools when available.

Personality:
- Professional
- Friendly
- Intelligent
- Respectful

Language:
- Arabic first.
- Support English when needed.
"""

    def format_history(self, history):
        """
        Convert conversation history into prompt text.
        """

        if not history:
            return ""

        text = "\n\nConversation history:\n"

        for message in history:

            role = message.get(
                "role",
                "user"
            )

            content = message.get(
                "content",
                ""
            )

            text += f"{role}: {content}\n"

        return text


    def format_prompt(self, user_message, history=None):
        """
        Build final model prompt.
        """

        prompt = self.system_prompt.strip()

        prompt += self.format_history(
            history
        )

        prompt += (
            f"\nUser: {user_message}"
            "\nNEURA-1:"
        )

        return prompt


if __name__ == "__main__":

    template = ChatTemplate()

    print(
        template.format_prompt(
            "مرحبا نيرا"
        )
    )