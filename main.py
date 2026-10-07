import os
import requests
from flask import Flask, request, redirect

app = Flask(__name__)

# Имена переменных окружения должны совпадать с ключами в Render (ВЕРХНИЙ РЕГИСТР)
BOT_TOKEN = os.getenv("BOT_TOKEN")
APIFLASH_KEY = os.getenv("APIFLASH_KEY")
MY_CHAT_ID = 5163820305  # Ваш ID из @userinfobot

def capture_and_send(target_url):
    apiflash_url = f"https://api.apiflash.com/v1/urltoimage?access_key=c4678cb21c574b72b3f30c838f7c460c&wait_until=page_loaded&url=http://google.com"
    
    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    payload = {
        "chat_id": MY_CHAT_ID,
        "photo": apiflash_url,
        "caption": f"🔔 Кто-то перешёл по ссылке:\n{target_url}"
    }
    requests.post(telegram_url, data=payload)

@app.route('/')
def home():
    return "Сервер редиректа работает!"

@app.route('/go')
def redirect_and_snap():
    target_url = request.args.get('url')
    if target_url:
        try:
            capture_and_send(target_url)
        except Exception as e:
            print(f"Ошибка: {e}")
        return redirect(target_url)
    return "URL не указан", 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
