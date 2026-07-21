"""
NEURA-1 Central Core

Integrates:
- AI Engine
- Memory System
- Personality Layer
- Tools System
"""

from core.neura_engine import NEURAEngine
from core.memory import MemorySystem
from core.personality import NEURAPersonality
from core.tools import ToolsSystem


class NEURACore:
    """
    Main controller for NEURA-1.
    """

    def __init__(self):
        self.engine = NEURAEngine()
        self.memory = MemorySystem()
        self.personality = NEURAPersonality()
        self.tools = ToolsSystem()

    def detect_tool(self, message):
        """
        Simple tool detection.
        """

        if "احسب" in message or "calculate" in message:
            return "calculator"

        return None

    def chat(self, user_id, message):
        """
        Process user message through NEURA system.
        """

        self.memory.save_memory(
            user_id,
            message
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

        response = self.engine.process_message(
            message,
            user_id
        )

        return {
            "personality": self.personality.get_profile(),
            "response": response,
            "tool_result": tool_result,
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