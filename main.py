from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "I'm alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Твой токен от BotFather
TOKEN = '7942840004:AAHM6DYSWCzXPLSMWVC2xBSATgW0WDZFC5I'

# Список ID групп
GROUP_IDS = [
    -1002505711094,  # Заменишь на свои ID
    ]

# Твой Telegram ID (узнай у @userinfobot)
OWNER_ID = 476397465

# Обработка команды /send
async def send_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("У тебя нет прав.")
        return

    text = ' '.join(context.args)
    if not text:
        await update.message.reply_text("Напиши текст после /send")
        return

    for chat_id in GROUP_IDS:
        await context.bot.send_message(chat_id=chat_id, text=text)

    await update.message.reply_text("Сообщения отправлены!")

# Запуск бота
if __name__ == '__main__':
    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(CommandHandler("send", send_message))

    keep_alive()  # запускаем веб-сервер
    app_bot.run_polling()
