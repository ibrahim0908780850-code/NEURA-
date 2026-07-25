"""
NEURA-1 Main Startup v0.9

Starts and initializes the NEURA-1 AI system.
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
            f"✅ Engine: {status.get('name', 'NEURA Engine')}"
        )


        print(
            f"📌 Version: {status.get('version', 'unknown')}"
        )


        print(
            f"🤖 Model: {status.get('model', 'unknown')}"
        )


        print(
            f"⚡ Inference Ready: {status.get('inference_ready', False)}"
        )


    except Exception as e:


        print(
            "⚠️ Engine status unavailable"
        )

        print(
            str(e)
        )


    systems = [

        "📚 Knowledge system",
        "💬 Conversation system",
        "🧠 Memory system",
        "🛠️ Tools system",
        "🔎 Web Search system",
        "💻 Code Agent"

    ]


    for system in systems:

        print(
            f"{system}: Ready"
        )




def print_banner():


    print(
"""
====================================

        🧠 NEURA-1 AI SYSTEM

        Arabic First AI Assistant

        Version: 0.9

====================================
"""
    )




def main():


    print_banner()


    try:


        initialize_neura()



        host = os.getenv(
            "HOST",
            "0.0.0.0"
        )



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