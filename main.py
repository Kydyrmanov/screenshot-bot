import os
import re
import urllib.parse
import telebot

# Получаем токены из системных переменных
BOT_TOKEN = os.environ.get("BOT_TOKEN")
APIFLASH_KEY = os.environ.get("APIFLASH_KEY")

bot = telebot.TeleBot(BOT_TOKEN)

# Регулярное выражение для поиска ссылок
URL_REGEX = r'https?://[^\s]+'

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Отправь мне ссылку (http:// или https://), и я сделаю её скриншот!")

@bot.message_handler(func=lambda message: True)
def process_message(message):
    match = re.search(URL_REGEX, message.text)
    if not match:
        return

    url = match.group(0)
    status_msg = bot.reply_to(message, "📸 Делаю скриншот, подождите...")

    try:
        encoded_url = urllib.parse.quote(url)
        screenshot_api_url = f"https://api.apiflash.com/v1/urltoimage?access_key={APIFLASH_KEY}&url={encoded_url}&width=1280&height=800"

        bot.send_photo(
            chat_id=message.chat.id,
            photo=screenshot_api_url,
            caption=f"Скриншот страницы:\n{url}",
            reply_to_message_id=message.message_id
        )
        bot.delete_message(message.chat.id, status_msg.message_id)

    except Exception as e:
        bot.edit_message_text("❌ Ошибка при создании скриншота.", message.chat.id, status_msg.message_id)

if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()