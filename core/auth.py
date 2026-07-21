"""
NEURA-1 Authentication System

Manages users and API access keys.
"""


import secrets
from datetime import datetime


class AuthSystem:
    """
    Basic authentication manager for NEURA-1.
    """

    def __init__(self):
        self.users = {}

    def create_user(self, user_id, name):
        """
        Create a new user.
        """

        api_key = secrets.token_hex(32)

        self.users[user_id] = {
            "name": name,
            "api_key": api_key,
            "created_at": datetime.utcnow().isoformat()
        }

        return self.users[user_id]

    def authenticate(self, api_key):
        """
        Verify API key.
        """

        for user_id, user in self.users.items():

            if user["api_key"] == api_key:
                return {
                    "authenticated": True,
                    "user_id": user_id
                }

        return {
            "authenticated": False
        }

    def get_user(self, user_id):
        """
        Get user information.
        """

        return self.users.get(user_id)


if __name__ == "__main__":

    auth = AuthSystem()

    user = auth.create_user(
        "demo-user",
        "Demo"
    )

    print(user)