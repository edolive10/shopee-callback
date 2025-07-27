from flask import Flask, request

app = Flask(__name__)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    return f"Code recebido: {code}", 200

@app.route("/")
def index():
    return "Servidor online com HTTPS ✅", 200
