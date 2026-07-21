"""
NEURA-1 Main Startup

Starts the NEURA-1 cloud system.
"""

import os
from dotenv import load_dotenv

from api.server import app


load_dotenv()


def main():
    """
    Start NEURA-1 API server.
    """

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))

    print("🤖 NEURA-1 is starting...")
    print(f"🌐 Server running on {host}:{port}")

    app.run(
        host=host,
        port=port
    )


if __name__ == "__main__":
    main()