from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    return f"Code recebido: {code}", 200

@app.route("/")
def index():
    return "Servidor online com HTTPS ✅", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
