"""
NEURA-1 Central Core

Integrates:
- AI Engine
- Conversation Manager
- Personality Layer
- Authentication Ready
"""

from core.neura_engine import NEURAEngine
from core.conversation import ConversationManager
from core.personality import NEURAPersonality
from core.tools import ToolsSystem


class NEURACore:
    """
    Main controller for NEURA-1.
    """

    def __init__(self):

        self.engine = NEURAEngine()

        self.conversation = ConversationManager()

        self.personality = NEURAPersonality()

        self.tools = ToolsSystem()


    def detect_tool(self, message):
        """
        Detect required tool.
        """

        if (
            "احسب" in message
            or "calculate" in message.lower()
        ):
            return "calculator"

        return None


    def chat(self, user_id, message):
        """
        Process user conversation.
        """


        self.conversation.add_message(
            user_id,
            "user",
            message
        )


        history = self.conversation.get_history(
            user_id
        )


        tool_result = None


        tool = self.detect_tool(
            message
        )


        if tool == "calculator":

            expression = (
                message
                .replace("احسب", "")
                .strip()
            )

            tool_result = self.tools.run_tool(
                "calculator",
                expression
            )


        response = self.engine.process_message(
            message,
            user_id,
            history
        )


        self.conversation.add_message(
            user_id,
            "assistant",
            str(response)
        )


        return {
            "personality": self.personality.get_profile(),

            "response": response,

            "tool_result": tool_result,

            "conversation": self.conversation.get_history(
                user_id
            ),

            "tools": self.tools.available_tools()
        }


if __name__ == "__main__":

    neura = NEURACore()

    result = neura.chat(
        "demo-user",
        "مرحبا نيرا"
    )

    print(result)