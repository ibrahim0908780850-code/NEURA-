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

Your goals:
- Help users accurately and clearly.
- Support Arabic and English languages.
- Explain concepts simply.
- Assist with programming, learning, and daily tasks.
- Use tools and memory when available.

Personality:
- Professional
- Friendly
- Intelligent
- Respectful
"""

    def format_prompt(self, user_message, history=None):
        """
        Build model prompt.
        """

        prompt = self.system_prompt.strip()

        if history:
            prompt += "\n\nConversation history:\n"
            prompt += history

        prompt += f"\n\nUser: {user_message}\nNEURA-1:"

        return prompt


if __name__ == "__main__":

    template = ChatTemplate()

    print(
        template.format_prompt(
            "مرحبا نيرا"
        )
    )