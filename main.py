import requests
import time
import hashlib
import hmac
import json

# ⚠️ Coloque suas credenciais reais aqui
client_id = "SEU_CLIENT_ID"
client_secret = "SEU_CLIENT_SECRET"
redirect_uri = "https://shopee-callback-6jxs.onrender.com/callback"

@app.route("/callback")
def callback():
    code = request.args.get("code")

    # Timestamp atual
    timestamp = int(time.time())

    # Base string para o HMAC
    base_string = f"{client_id}{redirect_uri}{code}{timestamp}"

    # Assinatura
    sign = hmac.new(
        client_secret.encode(),
        base_string.encode(),
        hashlib.sha256
    ).hexdigest()

    # Monta payload
    data = {
        "code": code,
        "partner_id": int(client_id),
        "shop_id": 0,  # opcional, só se já tiver
        "redirect_uri": redirect_uri,
        "sign": sign,
        "timestamp": timestamp
    }

    # Envia requisição
    resp = requests.post("https://partner.shopeemobile.com/api/v2/auth/token/get", json=data)

    # Retorna resposta bruta
    return f"Resposta Shopee: {resp.status_code}<br>{resp.text}", 200
