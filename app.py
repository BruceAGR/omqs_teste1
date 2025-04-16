from flask import Flask
import requests
from datetime import datetime, timedelta
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

@app.route("/")
def btc_notifier():
    agora = datetime.utcnow() - timedelta(hours=3)  # Corrige fuso para BRT
    agora_str = agora.strftime('%d/%m/%Y %H:%M:%S')

    # Consulta o preço do BTC (via CoinGecko)
    r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=brl")
    btc_price = r.json().get("bitcoin", {}).get("brl", "N/A")

    # Mensagem
    msg = f"💰 BTC está em R$ {btc_price:,} — {agora_str}"

    # Enviar para Telegram
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg}
    res = requests.post(url, data=payload)

    return f"Enviado: {msg} | Status: {res.status_code}"
