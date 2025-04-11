import requests
import os

TOKEN = os.getenv('TELEGRAM_TOKEN')      # Pega do GitHub Secrets
chat_id = os.getenv('TELEGRAM_CHAT_ID')      # Pega do GitHub Secrets
mensagem = '🚀 Notificação enviada do Google Colab!2'

url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
payload = {
    'chat_id': chat_id,
    'text': mensagem
}

res = requests.post(url, data=payload)

print(res.status_code)
print(res.text)

if res.status_code == 200:
    print("✅ Mensagem enviada com sucesso2!")
else:
    print("❌ Erro ao enviar:", res.text)
