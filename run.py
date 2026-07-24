"""
NEURA-1 Main Startup

Starts and initializes the NEURA-1 system.
"""

import os
import traceback


from api.server import app, neura



def initialize_neura():
    """
    Initialize NEURA-1 components.
    """

    print("🧠 Initializing NEURA-1...")


    try:

        status = neura.engine.get_status()


        print(
            f"✅ Engine: {status.get('name','NEURA Engine')}"
        )

        print(
            f"📌 Version: {status.get('version','unknown')}"
        )

        print(
            f"🤖 Model: {status.get('model','unknown')}"
        )


    except Exception as e:

        print(
            "⚠️ Engine status unavailable:"
        )

        print(e)



    print("📚 Knowledge system: Ready")
    print("💬 Conversation system: Ready")
    print("🧠 Memory system: Ready")
    print("🛠️ Tools system: Ready")
    print("🔎 Web Search system: Ready")
    print("💻 Code Agent: Ready")




def print_banner():

    print("""
================================

        NEURA-1 AI SYSTEM

        Advanced AI Assistant

================================
""")




def main():

    print_banner()


    try:

        initialize_neura()


        host = os.getenv(
            "HOST",
            "0.0.0.0"
        )


        # Railway injects PORT automatically

        port = int(
            os.getenv(
                "PORT",
                8080
            )
        )


        print(
            f"🌐 Server running on {host}:{port}"
        )


        app.run(

            host=host,

            port=port,

            debug=False,

            threaded=True

        )


    except Exception:


        print(
            "❌ NEURA failed to start"
        )


        traceback.print_exc()



if __name__ == "__main__":

    main()