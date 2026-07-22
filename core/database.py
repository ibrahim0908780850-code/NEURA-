import os
from supabase import create_client


class Database:

    def __init__(self):

        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

        if not url or not key:
            raise Exception(
                "Supabase credentials missing"
            )

        self.client = create_client(
            url,
            key
        )


db = Database()