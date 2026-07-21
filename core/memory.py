"""
NEURA-1 Memory System

Handles user context, conversations, and long-term memory.
"""

from datetime import datetime


class MemorySystem:
    """
    Basic memory layer for NEURA-1.
    """

    def __init__(self):
        self.memories = []

    def save_memory(self, user_id, content):
        """
        Store user information or conversation context.
        """

        memory = {
            "user_id": user_id,
            "content": content,
            "created_at": datetime.utcnow().isoformat()
        }

        self.memories.append(memory)

        return memory

    def get_memories(self, user_id):
        """
        Retrieve memories for a specific user.
        """

        return [
            memory
            for memory in self.memories
            if memory["user_id"] == user_id
        ]


if __name__ == "__main__":

    memory = MemorySystem()

    memory.save_memory(
        "demo-user",
        "User prefers Arabic language"
    )

    print(memory.get_memories("demo-user"))