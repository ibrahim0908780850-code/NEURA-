"""
NEURA-1 Main Startup

Starts and initializes the NEURA-1 cloud system.
"""

import os

from dotenv import load_dotenv

from api.server import app, neura


load_dotenv()


def initialize_neura():
    """
    Initialize NEURA-1 components.
    """

    print("🧠 Initializing NEURA-1...")

    status = neura.engine.get_status()

    print(
        f"✅ Engine: {status['name']}"
    )

    print(
        f"📌 Version: {status['version']}"
    )

    print(
        "📚 Knowledge system: Ready"
    )

    print(
        "💬 Conversation system: Ready"
    )

    print(
        "🛠️ Tools system: Ready"
    )


def main():
    """
    Start NEURA-1 API server.
    """

    host = os.getenv(
        "HOST",
        "0.0.0.0"
    )

    port = int(
        os.getenv(
            "PORT",
            8000
        )
    )

    print("""
================================
        NEURA-1 AI SYSTEM
================================
    """)

    initialize_neura()

    print(
        f"🌐 Server running on {host}:{port}"
    )

    app.run(
        host=host,
        port=port,
        debug=False
    )


if __name__ == "__main__":
    main()