"""
NEURA-1 Cloud API Server

Provides communication between applications and NEURA core.
"""

from flask import Flask, request, jsonify

from core.neura_core import NEURACore


app = Flask(__name__)

neura = NEURACore()


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "name": "NEURA-1",
        "status": "online",
        "version": "0.1.0"
    })


@app.route("/api/chat", methods=["POST"])
def chat():

    data = request.json

    user_id = data.get("user_id", "guest")
    message = data.get("message", "")

    response = neura.chat(
        user_id,
        message
    )

    return jsonify(response)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000
    )