import requests

TOKEN = '7488164113:AAEXiG5Xl-UpYChI4ASDBmMaZS3rEIwpoUc'  # Seu token
chat_id = '331126754'
mensagem = '🚀 Notificação enviada do Google Colab!2'

url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
payload = {
    'chat_id': chat_id,
    'text': mensagem
}

res = requests.post(url, data=payload)

if res.status_code == 200:
    print("✅ Mensagem enviada com sucesso2!")
else:
    print("❌ Erro ao enviar:", res.text)
