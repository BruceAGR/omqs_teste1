from flask import Flask
import requests
from datetime import datetime
import os

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

@app.route("/")
def notify():
    agora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    mensagem = f'⏰ Notificação às {agora} (enviada via cron-job.org)'

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": mensagem
    }

    res = requests.post(url, data=payload)
    return f"Status: {res.status_code} - {res.text}"
