from flask import Flask
import requests
from datetime import datetime, timedelta
import os
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# Variáveis de ambiente
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GOOGLE_SHEETS_KEY = os.getenv("GOOGLE_SHEETS_KEY")

# Autenticação com Google Sheets
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_file("credenciais.json", scopes=scopes)
gc = gspread.authorize(credentials)
sheet = gc.open_by_key(GOOGLE_SHEETS_KEY).worksheet("Página1")

@app.route("/")
def btc_notifier():
    agora = datetime.utcnow() - timedelta(hours=3)
    agora_str = agora.strftime('%d/%m/%Y %H:%M:%S')

    # Preço do BTC
    r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=brl")
    btc_price = r.json().get("bitcoin", {}).get("brl", 0)

    # Salva no Google Sheets
    sheet.append_row([agora_str, btc_price])

    # Envia mensagem Telegram
    msg = f"💰 BTC está em R$ {btc_price:,.2f} — {agora_str}"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg}
    res = requests.post(url, data=payload)

    return f"✅ Enviado: {msg} | Google Sheets atualizado! Status: {res.status_code}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
