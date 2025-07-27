from flask import Flask, request
import requests
import time
import hashlib
import hmac
import json
import os

app = Flask(__name__)

# 🔐 Credenciais reais da Shopee
client_id = "18312200188"
client_secret = "KYX252AE6AHCSTENQCRKTH4SAGFFHFDQ"
redirect_uri = "https://shopee-callback-6jxs.onrender.com/callback"

@app.route("/")
def index():
    return "Servidor online com HTTPS ✅", 200

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "Código não fornecido", 400

    # Gera timestamp válido (até 32 bits)
    timestamp = int(time.time()) % 4294967296

    # Monta string base para assinatura
    base_string = f"{client_id}{redirect_uri}{code}{timestamp}"
    sign = hmac.new(client_secret.encode(), base_string.encode(), hashlib.sha256).hexdigest()

    # Corpo da requisição
    payload = {
        "code": code,
        "partner_id": int(client_id),
        "redirect_uri": redirect_uri,
        "sign": sign,
        "timestamp": timestamp
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            "https://partner.shopeemobile.com/api/v2/auth/token/get",
            headers=headers,
            json=payload,
            timeout=10
        )
        data = response.json()
    except Exception as e:
        return f"Erro ao chamar a API da Shopee: {e}", 500

    if "access_token" not in data:
        return f"Erro na resposta da Shopee: {data}", 400

    # Salva token
    with open("token.json", "w") as f:
        json.dump(data, f, indent=2)

    return f"Token salvo com sucesso!<br>Shop ID: {data.get('shop_id')}", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

