"""
NEURA-1 Main Startup

Starts and initializes the NEURA-1 system.
"""

from config import Config
from api.server import app, neura


config = Config()


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
        f"🤖 Model: {status['model']}"
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


    print("""
================================
        NEURA-1 AI SYSTEM
================================
""")


    initialize_neura()


    print(
        f"🌐 Server running on {config.host}:{config.port}"
    )


    app.run(
        host=config.host,
        port=config.port,
        debug=False
    )


if __name__ == "__main__":

    main()