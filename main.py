import requests
import os
from datetime import datetime  # 👈 importa o datetime

# Pega as variáveis de ambiente (se quiser usar Secrets do GitHub futuramente)
TOKEN = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')

# Pega o horário atual formatado
agora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

# Mensagem com horário
mensagem = f'🚀 Notificação enviada do GitHub Actions às {agora}!'

url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
payload = {
    'chat_id': chat_id,
    'text': mensagem
}

res = requests.post(url, data=payload)

print(res.status_code)
print(res.text)

if res.status_code == 200:
    print(mensagem)
else:
    print("❌ Erro ao enviar:", res.text)
