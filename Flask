import json
import base64
import time
import uuid
from flask import Flask, request, jsonify

app = Flask(__name__)

# -------------------- helpers --------------------

def get_uuid_hex():
    return uuid.uuid4().hex

def b64encode_json(obj):
    return base64.urlsafe_b64encode(
        json.dumps(obj).encode()
    ).decode().rstrip("=")

def generate_token(username, agent, nonce, loginType, userid):
    header = {"alg": "none", "typ": "JWT"}
    now = int(time.time())

    payload = {
        "tid": get_uuid_hex(),
        "uid": userid or get_uuid_hex(),
        "usn": username or "Player",
        "vrs": {
            "authID": nonce,
            "clientUserAgent": agent,
            "loginType": loginType,
            "deviceID": "Android"
        },
        "iat": now,
        "exp": now + 9999999
    }

    return f"{b64encode_json(header)}.{b64encode_json(payload)}."

# -------------------- auth --------------------

@app.route("/v2/account/authenticate/custom", methods=["POST"])
def authenticate():
    data = request.get_json(silent=True) or {}
    vars_data = data.get("vars", {})
    vars_data = vars_data[0] if isinstance(vars_data, list) and vars_data else vars_data

    token = generate_token(
        request.args.get("username", "Alex"),
        vars_data.get("clientUserAgent", ""),
        vars_data.get("nonce", ""),
        vars_data.get("loginType", ""),
        data.get("id", get_uuid_hex())
    )

    return jsonify({
        "success": True,
        "token": token
    })

@app.route("/v2/account/session/refresh", methods=["POST"])
def session_refresh():
    return jsonify({"success": True})

# -------------------- account --------------------

@app.route("/v2/account", methods=["GET", "PUT"])
def account():
    return jsonify({
        "user": {
            "id": get_uuid_hex(),
            "username": "Alex",
            "display_name": "Alex",
            "lang_tag": "en",
            "metadata": {
                "isDeveloper": True,
                "bypassed": True
            },
            "edge_count": 1,
            "create_time": "2024-08-24T04:20:56Z",
            "update_time": "2025-07-25T18:41:17Z"
        },
        "wallet": {
            "stashCols": 12,
            "stashRows": 12,
            "hardCurrency": 9999999,
            "softCurrency": 9999999,
            "researchPoints": 9999999
        }
    })

# -------------------- storage --------------------

@app.route("/v2/storage", methods=["GET", "POST", "PUT"])
def storage():
    return jsonify({"objects": []})

# -------------------- purchases --------------------

@app.route("/v2/rpc/purchase.list", methods=["POST"])
def purchase_list():
    return jsonify({
        "payload": {
            "purchases": []
        }
    })

@app.route("/v2/rpc/getStore", methods=["POST"])
def get_store():
    return jsonify({
        "payload": {
            "enabled": True,
            "products": []
        }
    })

# -------------------- remote config --------------------

@app.route("/v2/rpc/getRemoteConfig", methods=["POST"])
def get_remote_config():
    return jsonify({
        "payload": {
            "maintenance": False,
            "forceUpdate": False,
            "minVersion": "1.17.0"
        }
    })

# -------------------- bootstrap (CRITICAL) --------------------

@app.route("/v2/rpc/clientBootstrap", methods=["GET", "POST"])
def client_bootstrap():
    return jsonify({
        "success": True,
        "updateType": "None",
        "maintenance": False,
        "attestResult": "Valid",
        "attestTokenExpiresAt": 2000000000,
        "serverTimeUnix": int(time.time()),

        "nakama": {
            "enabled": True,
            "host": "127.0.0.1",
            "port": 7350,
            "ssl": False
        },

        "store": {
            "enabled": True
        },

        "features": {},
        "config": {},
        "economy": {}
    })

# -------------------- run --------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
