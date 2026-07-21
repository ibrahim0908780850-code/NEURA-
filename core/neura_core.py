"""
NEURA-1 Central Core

Integrates:
- AI Engine
- Memory System
- Conversation Manager
- Personality Layer
- Knowledge System
- Tools System
"""

from core.neura_engine import NEURAEngine
from core.memory import MemorySystem
from core.conversation import ConversationManager
from core.personality import NEURAPersonality
from core.knowledge import KnowledgeBase
from core.tools import ToolsSystem


class NEURACore:
    """
    Main controller for NEURA-1.
    """

    def __init__(self):
        self.engine = NEURAEngine()

        self.memory = MemorySystem()
        self.conversation = ConversationManager()

        self.personality = NEURAPersonality()
        self.knowledge = KnowledgeBase()
        self.tools = ToolsSystem()

    def detect_tool(self, message):
        """
        Detect if user needs a tool.
        """

        if "احسب" in message or "calculate" in message:
            return "calculator"

        return None

    def chat(self, user_id, message):
        """
        Process user message through NEURA system.
        """

        # Save conversation
        self.conversation.add_message(
            user_id,
            "user",
            message
        )

        # Save memory
        self.memory.save_memory(
            user_id,
            message
        )

        # Get conversation history
        history = self.conversation.get_history(
            user_id
        )

        tool_result = None

        tool = self.detect_tool(message)

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

        # Generate AI response
        response = self.engine.process_message(
            message,
            user_id
        )

        # Save assistant response
        self.conversation.add_message(
            user_id,
            "assistant",
            str(response)
        )

        return {
            "personality": self.personality.get_profile(),
            "response": response,
            "tool_result": tool_result,
            "conversation": history,
            "available_tools": self.tools.available_tools(),
            "memory": self.memory.get_memories(user_id)
        }


if __name__ == "__main__":

    neura = NEURACore()

    result = neura.chat(
        "demo-user",
        "مرحبا نيرا"
    )

    print(result)