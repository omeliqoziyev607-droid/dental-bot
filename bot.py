import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime

TOKEN = "7874069508:AAFTXxSlRM45b-5TsCEENtDkRxD7HuuAnj4"

appointments = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom! Navbat qoshish uchun yozing:
"
        "Ism: Aliyev Vohid
"
        "Soat: 14:30
"
        "Sana: 29.05.2026"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    lines = text.strip().split('
')
    data = {}
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            data[key.strip().lower()] = value.strip()
    
    if 'ism' in data and 'soat' in data:
        appointment = {
            "name": data.get('ism', ''),
            "time": data.get('soat', ''),
            "date": data.get('sana', datetime.now().strftime('%d.%m.%Y')),
            "timestamp": datetime.now().isoformat()
        }
        appointments.append(appointment)
        await update.message.reply_text(
            "Navbat qoshildi!
"
            "Bemor: " + appointment['name'] + "
"
            "Soat: " + appointment['time'] + "
"
            "Sana: " + appointment['date']
        )
    else:
        await update.message.reply_text(
            "Format notogri!

"
            "Quyidagicha yozing:
"
            "Ism: Aliyev Vohid
"
            "Soat: 14:30
"
            "Sana: 29.05.2026"
        )

async def get_appointments(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not appointments:
        await update.message.reply_text("Navbatlar yoq")
        return
    text = "Bugungi navbatlar:

"
    for i, a in enumerate(appointments, 1):
        text += str(i) + ". " + a['name'] + " - " + a['time'] + " (" + a['date'] + ")
"
    await update.message.reply_text(text)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("navbatlar", get_appointments))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
