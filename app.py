from flask import Flask
import requests
from datetime import datetime, timedelta
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Variáveis de ambiente
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GOOGLE_SHEETS_KEY = os.getenv("GOOGLE_SHEETS_KEY")

# Setup do Google Sheets
def salvar_em_sheets(data, preco):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json", scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_key(GOOGLE_SHEETS_KEY)
    aba = sheet.worksheet("Página1")
    aba.append_row([data, preco])

@app.route("/")
def btc_notifier():
    agora = datetime.utcnow() - timedelta(hours=3)  # BRT
    agora_str = agora.strftime('%d/%m/%Y %H:%M:%S')

    # Preço BTC via CoinGecko
    r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=brl")
    btc_price = r.json().get("bitcoin", {}).get("brl")

    if btc_price is None:
        return "Erro ao obter preço do BTC"

    # Salvar no Google Sheets
    salvar_em_sheets(agora_str, btc_price)

    # Enviar Telegram
    msg = f"💰 BTC está em R$ {btc_price:,} — {agora_str}"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg}
    res = requests.post(url, data=payload)

    return f"Enviado: {msg} | Status: {res.status_code}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
