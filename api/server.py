"""
NEURA-1 Cloud API Server

Provides secure communication between applications
and NEURA core.
"""

from flask import Flask, request, jsonify

from core.config import Config
from core.neura_core import NEURACore
from core.auth import AuthSystem


app = Flask(__name__)

config = Config()

neura = NEURACore()
auth = AuthSystem()


@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "name": config.app_name,
        "status": "online",
        "version": config.version,
        "description": "Arabic-first cloud AI system"
    })


@app.route("/api/status", methods=["GET"])
def status():

    return jsonify(
        neura.engine.get_status()
    )


@app.route("/api/user/create", methods=["POST"])
def create_user():

    data = request.json or {}

    user_id = data.get("user_id")
    name = data.get(
        "name",
        "User"
    )

    if not user_id:

        return jsonify({
            "error": "user_id required"
        }), 400


    user = auth.create_user(
        user_id,
        name
    )

    return jsonify(user)



@app.route("/api/chat", methods=["POST"])
def chat():

    try:

        data = request.json or {}

        api_key = data.get(
            "api_key"
        )


        if api_key:

            check = auth.authenticate(
                api_key
            )

            if not check["authenticated"]:

                return jsonify({
                    "error": "Invalid API key"
                }), 401


            user_id = check["user_id"]

        else:

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
                "error": "message required"
            }), 400



        response = neura.chat(
            user_id,
            message
        )


        return jsonify(
            response
        )


    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500



if __name__ == "__main__":

    app.run(
        host=config.host,
        port=config.port,
        debug=False
    )