"""
NEURA-1 Cloud API Server v0.9

Secure API Gateway for NEURA-1.

Features:
- Chat API
- Status API
- Code Agent
- User Management
- Health Check
"""


from flask import Flask, request, jsonify
from flask_cors import CORS

from core.config import Config
from core.neura_core import NEURACore
from core.auth import AuthSystem



# =========================
# App
# =========================

app = Flask(__name__)

CORS(app)



# =========================
# Core Systems
# =========================

config = Config()


try:

    neura = NEURACore()

    auth = AuthSystem()


    print(
        "✅ NEURA Core initialized"
    )


except Exception as e:

    print(
        "❌ NEURA initialization failed:"
    )

    print(e)


    neura = None
    auth = None





# =========================
# Home
# =========================

@app.route("/", methods=["GET"])
def home():

    return jsonify({

        "name": "NEURA-1",

        "status": "online",

        "version": "0.9.0",

        "description":
        "Arabic-first AI Cloud System"

    })





# =========================
# Status
# =========================

@app.route(
    "/api/status",
    methods=["GET"]
)
def status():

    if not neura:

        return jsonify({

            "status":
            "failed"

        }), 500



    return jsonify(

        neura.engine.get_status()

    )





# =========================
# Health
# =========================

@app.route(
    "/api/health",
    methods=["GET"]
)
def health():

    if not neura:

        return jsonify({

            "healthy":
            False

        })


    return jsonify(

        neura.engine.health()

    )





# =========================
# Create User
# =========================

@app.route(
    "/api/user/create",
    methods=["POST"]
)
def create_user():

    data = request.json or {}


    user_id = data.get(
        "user_id"
    )


    name = data.get(
        "name",
        "User"
    )


    if not user_id:

        return jsonify({

            "error":
            "user_id required"

        }), 400



    return jsonify(

        auth.create_user(
            user_id,
            name
        )

    )





# =========================
# Chat
# =========================

@app.route(
    "/api/chat",
    methods=["POST"]
)
def chat():

    try:

        if not neura:

            return jsonify({

                "error":
                "NEURA unavailable"

            }), 500



        data = request.json or {}


        user_id = data.get(
            "user_id",
            "guest"
        )


        message = data.get(
            "message",
            ""
        )


        if not message:

            return jsonify({

                "error":
                "message required"

            }), 400



        result = neura.chat(

            user_id,

            message

        )


        return jsonify(result)



    except Exception as e:

        return jsonify({

            "error":
            str(e)

        }), 500





# =========================
# Code Agent
# =========================

@app.route(
    "/api/code",
    methods=["POST"]
)
def code():

    try:

        if not neura:

            return jsonify({

                "error":
                "NEURA unavailable"

            }), 500



        data = request.json or {}


        source = data.get(
            "code",
            ""
        )


        action = data.get(
            "action",
            "analyze"
        )


        if not source:

            return jsonify({

                "error":
                "code required"

            }), 400



        agent = neura.engine.code_agent



        if action == "fix":


            result = agent.fix(

                source,

                neura.engine

            )


        elif action == "analyze":


            result = agent.analyze(

                source

            )


        elif action == "explain":


            result = agent.explain(

                source

            )


        else:


            result = {

                "error":
                "unknown action"

            }



        return jsonify(result)



    except Exception as e:


        return jsonify({

            "error":
            str(e)

        }), 500





# =========================
# Run Server
# =========================

if __name__ == "__main__":

    app.run(

        host=config.host,

        port=config.port,

        debug=False

    )