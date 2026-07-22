"""
NEURA-1 Memory System

Handles short-term and long-term memory
using Supabase persistent storage.
"""

from datetime import datetime
from core.database import db


class MemorySystem:
    """
    Memory layer for NEURA-1.
    """


    def __init__(self):
        self.table = "memories"


    def save_memory(
        self,
        user_id,
        content,
        memory_type="short_term",
        importance="normal"
    ):
        """
        Store user memory in Supabase.
        """

        memory = {
            "user_id": user_id,
            "memory": content,
            "type": memory_type,
            "importance": importance,
            "created_at": datetime.utcnow().isoformat()
        }


        result = (
            db.client
            .table(self.table)
            .insert(memory)
            .execute()
        )


        return result.data[0] if result.data else memory



    def get_memories(self, user_id):
        """
        Retrieve user memories.
        """

        result = (
            db.client
            .table(self.table)
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )


        return result.data



    def search_memory(self, user_id, query):
        """
        Search user memories.
        """

        result = (
            db.client
            .table(self.table)
            .select("*")
            .eq("user_id", user_id)
            .ilike(
                "memory",
                f"%{query}%"
            )
            .execute()
        )


        return result.data



    def clear_memory(self, user_id):
        """
        Delete user memories.
        """

        result = (
            db.client
            .table(self.table)
            .delete()
            .eq("user_id", user_id)
            .execute()
        )


        return result.data



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