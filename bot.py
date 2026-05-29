import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime

TOKEN = "7874069508:AAFTXxSlRM45b-5TsCEENtDkRxD7HuuAnj4"
appointments = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "Salom! Navbat qoshish uchun yozing:\nIsm: Aliyev Vohid\nSoat: 14:30\nSana: 29.05.2026"
    await update.message.reply_text(msg)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    data = {}
    for line in text.strip().split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            data[k.strip().lower()] = v.strip()
    if "ism" in data and "soat" in data:
        a = {
            "name": data["ism"],
            "time": data["soat"],
            "date": data.get("sana", datetime.now().strftime("%d.%m.%Y")),
            "timestamp": datetime.now().isoformat()
        }
        appointments.append(a)
        msg = "Navbat qoshildi!\nBemor: " + a["name"] + "\nSoat: " + a["time"] + "\nSana: " + a["date"]
        await update.message.reply_text(msg)
    else:
        msg = "Format notogri!\nQuyidagicha yozing:\nIsm: Aliyev Vohid\nSoat: 14:30\nSana: 29.05.2026"
        await update.message.reply_text(msg)

async def get_appointments(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not appointments:
        await update.message.reply_text("Navbatlar yoq")
        return
    t = "Bugungi navbatlar:\n"
    for i, a in enumerate(appointments, 1):
        t += str(i) + ". " + a["name"] + " - " + a["time"] + " (" + a["date"] + ")\n"
    await update.message.reply_text(t)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("navbatlar", get_appointments))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
