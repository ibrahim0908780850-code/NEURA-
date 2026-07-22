"""
NEURA-1 Conversation Manager

Manages user sessions and conversation history
using Supabase persistent storage.
"""

from datetime import datetime
from core.database import db


class ConversationManager:
    """
    Handles conversation sessions for NEURA-1.
    """


    def __init__(self):
        self.conversation_table = "conversations"
        self.message_table = "messages"



    def create_session(self, user_id, title="NEURA Conversation"):
        """
        Create a new conversation session.
        """

        result = (
            db.client
            .table(self.conversation_table)
            .insert({
                "user_id": user_id,
                "title": title,
                "created_at": datetime.utcnow().isoformat()
            })
            .execute()
        )


        return result.data[0] if result.data else None



    def get_or_create_session(self, user_id):
        """
        Get existing conversation or create one.
        """

        result = (
            db.client
            .table(self.conversation_table)
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )


        if result.data:
            return result.data[0]


        return self.create_session(user_id)



    def add_message(self, user_id, role, content):
        """
        Save message permanently.
        """

        session = self.get_or_create_session(
            user_id
        )


        message = {
            "conversation_id": session["id"],
            "role": role,
            "content": content,
            "created_at": datetime.utcnow().isoformat()
        }


        result = (
            db.client
            .table(self.message_table)
            .insert(message)
            .execute()
        )


        return result.data[0] if result.data else None



    def get_history(self, user_id):
        """
        Retrieve conversation history.
        """

        session = self.get_or_create_session(
            user_id
        )


        result = (
            db.client
            .table(self.message_table)
            .select("*")
            .eq(
                "conversation_id",
                session["id"]
            )
            .order(
                "created_at"
            )
            .execute()
        )


        return [
            {
                "role": item["role"],
                "content": item["content"],
                "timestamp": item["created_at"]
            }
            for item in result.data
        ]



    def clear_session(self, user_id):
        """
        Delete user conversation.
        """

        sessions = (
            db.client
            .table(self.conversation_table)
            .select("id")
            .eq("user_id", user_id)
            .execute()
        )


        for session in sessions.data:

            db.client.table(
                self.message_table
            ).delete().eq(
                "conversation_id",
                session["id"]
            ).execute()


        return True



if __name__ == "__main__":

    conversation = ConversationManager()

    conversation.add_message(
        "demo-user",
        "user",
        "مرحبا نيرا"
    )

    conversation.add_message(
        "demo-user",
        "assistant",
        "مرحبا! كيف يمكنني مساعدتك؟"
    )


    print(
        conversation.get_history(
            "demo-user"
        )
    )