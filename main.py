import requests
import os

TOKEN = os.getenv('BOT_TOKEN')         # nome do secret no GitHub
chat_id = os.getenv('CHAT_ID')         # nome do secret no GitHub
mensagem = '🚀 Notificação enviada do Google Colab!2'

url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
payload = {
    'chat_id': chat_id,
    'text': mensagem
}

res = requests.post(url, data=payload)

print(res.status_code)
print(res.text)

print(TOKEN)
print(chat_id)

if res.status_code == 200:
    print("✅ Mensagem enviada com sucesso2!")
else:
    print("❌ Erro ao enviar:", res.text)
