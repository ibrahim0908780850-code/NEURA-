"""
NEURA-1 Central Core

Integrates:
- AI Engine
- Memory System
- Personality Layer
"""

from core.neura_engine import NEURAEngine
from core.memory import MemorySystem
from core.personality import NEURAPersonality


class NEURACore:
    """
    Main controller for NEURA-1.
    """

    def __init__(self):
        self.engine = NEURAEngine()
        self.memory = MemorySystem()
        self.personality = NEURAPersonality()

    def chat(self, user_id, message):
        """
        Process user message through NEURA system.
        """

        self.memory.save_memory(
            user_id,
            message
        )

        response = self.engine.process_message(
            message,
            user_id
        )

        return {
            "personality": self.personality.get_profile(),
            "response": response,
            "memory": self.memory.get_memories(user_id)
        }


if __name__ == "__main__":

    neura = NEURACore()

    result = neura.chat(
        "demo-user",
        "مرحبا نيرا"
    )

    print(result)