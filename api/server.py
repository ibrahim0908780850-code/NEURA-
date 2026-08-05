"""
NEURA-1 Cloud API Server v1.0

Backend Gateway for NEURA-1 Frontend

Features:
- Chat API
- Status API
- Health Check
- User Management
- Code Agent
- Frontend Integration
"""


from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

from core.config import Config
from core.neura_core import NEURACore
from core.auth import AuthSystem



# =========================
# App
# =========================

app = Flask(__name__)


# Frontend Access

CORS(
    app,
    resources={
        r"/api/*":{
            "origins":"*"
        }
    }
)



# =========================
# Core
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
        "❌ NEURA initialization failed",
        e
    )

    neura = None
    auth = None





# =========================
# API Root
# =========================

@app.route("/")
def home():

    return jsonify({

        "name":"NEURA-1",

        "version":"1.0.0",

        "status":"online",

        "message":
        "Arabic-first AI Cloud System",

        "time":
        datetime.utcnow().isoformat()

    })





# =========================
# System Status
# =========================

@app.route(
"/api/status",
methods=["GET"]
)
def status():


    if not neura:

        return jsonify({

            "status":"offline"

        }),500



    return jsonify({

        "status":"online",

        "version":"1.0.0",

        "engine":
        neura.engine.get_status()

    })





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

            "healthy":False

        })


    return jsonify({

        "healthy":True,

        "service":"NEURA-1",

        "time":
        datetime.utcnow().isoformat()

    })





# =========================
# User Create
# =========================

@app.route(
"/api/user/create",
methods=["POST"]
)
def create_user():


    data=request.json or {}


    user_id=data.get(
        "user_id"
    )


    name=data.get(
        "name",
        "User"
    )


    if not user_id:

        return jsonify({

            "error":
            "user_id required"

        }),400



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

            }),500



        data=request.json or {}


        message=data.get(
            "message",
            ""
        )


        user_id=data.get(
            "user_id",
            "guest"
        )


        if not message:

            return jsonify({

                "error":
                "message required"

            }),400



        result=neura.chat(

            user_id,

            message

        )


        return jsonify({

            "success":True,

            "response":result,

            "time":
            datetime.utcnow().isoformat()

        })



    except Exception as e:


        return jsonify({

            "success":False,

            "error":
            str(e)

        }),500





# =========================
# Code Agent
# =========================

@app.route(
"/api/code",
methods=["POST"]
)
def code():


    try:


        data=request.json or {}


        source=data.get(
            "code",
            ""
        )


        action=data.get(
            "action",
            "analyze"
        )


        if not source:

            return jsonify({

                "error":
                "code required"

            }),400



        agent=neura.engine.code_agent



        if action=="fix":

            result=agent.fix(
                source,
                neura.engine
            )


        elif action=="analyze":

            result=agent.analyze(
                source
            )


        elif action=="explain":

            result=agent.explain(
                source
            )


        else:

            result={
                "error":
                "unknown action"
            }



        return jsonify({

            "success":True,

            "result":result

        })


    except Exception as e:


        return jsonify({

            "success":False,

            "error":str(e)

        }),500





# =========================
# Run
# =========================

if __name__=="__main__":


    app.run(

        host=config.host,

        port=config.port,

        debug=False

    )