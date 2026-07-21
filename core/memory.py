"""
NEURA-1 Memory System

Handles short-term and long-term memory
for users and conversations.
"""

from datetime import datetime


class MemorySystem:
    """
    Memory layer for NEURA-1.
    """

    def __init__(self):

        self.memories = []


    def save_memory(
        self,
        user_id,
        content,
        memory_type="short_term",
        importance="normal"
    ):
        """
        Store user memory.
        """

        memory = {
            "user_id": user_id,
            "content": content,
            "type": memory_type,
            "importance": importance,
            "created_at": datetime.utcnow().isoformat()
        }

        self.memories.append(
            memory
        )

        return memory


    def get_memories(self, user_id):
        """
        Retrieve memories for user.
        """

        return [
            memory
            for memory in self.memories
            if memory["user_id"] == user_id
        ]


    def search_memory(self, user_id, query):
        """
        Search user memories.
        """

        query = query.lower()

        return [
            memory
            for memory in self.get_memories(user_id)
            if query in memory["content"].lower()
        ]


    def clear_memory(self, user_id):
        """
        Delete user memories.
        """

        self.memories = [
            memory
            for memory in self.memories
            if memory["user_id"] != user_id
        ]


if __name__ == "__main__":

    memory = MemorySystem()

    memory.save_memory(
        "demo-user",
        "User prefers Arabic language",
        "long_term",
        "high"
    )

    print(
        memory.get_memories(
            "demo-user"
        )
    )