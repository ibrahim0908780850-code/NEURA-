"""
NEURA-1 Conversation Manager

Manages user sessions and conversation history.
"""

from datetime import datetime


class ConversationManager:
    """
    Handles conversation sessions for NEURA-1.
    """

    def __init__(self):
        self.sessions = {}

    def create_session(self, user_id):
        """
        Create a new conversation session.
        """

        if user_id not in self.sessions:
            self.sessions[user_id] = []

        return {
            "user_id": user_id,
            "status": "created"
        }

    def add_message(self, user_id, role, content):
        """
        Add message to conversation history.
        """

        if user_id not in self.sessions:
            self.create_session(user_id)

        self.sessions[user_id].append({
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        })

    def get_history(self, user_id):
        """
        Retrieve conversation history.
        """

        return self.sessions.get(
            user_id,
            []
        )

    def clear_session(self, user_id):
        """
        Remove conversation history.
        """

        if user_id in self.sessions:
            del self.sessions[user_id]


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