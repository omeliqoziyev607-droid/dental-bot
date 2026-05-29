import os
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime

TOKEN = "7874069508:AAFTXxSlRM45b-5TsCEENtDkRxD7HuuAnj4"
DATA_FILE = "appointments.json"

def load_appointments():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_appointments(appointments):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(appointments, f, ensure_ascii=False, indent=2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "Salom! Navbat qoshish uchun yozing:\nIsm: Aliyev Vohid\nSoat: 14:30\nSana: 29.05.2026"
    await update.message.reply_text(msg)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    data = {}
    for line in text.strip().split("\n"):
        if ":" in line:
            parts = line.split(":", 1)
            key = parts[0].strip().lower()
            value = parts[1].strip()
            data[key] = value
    if "ism" in data and "soat" in data:
        appointment = {
            "name": data["ism"],
            "time": data["soat"],
            "date": data.get("sana", datetime.now().strftime("%d.%m.%Y")),
            "timestamp": datetime.now().isoformat()
        }
        appointments = load_appointments()
        appointments.append(appointment)
        save_appointments(appointments)
        msg = "Navbat qoshildi!\nBemor: " + appointment["name"] + "\nSoat: " + appointment["time"] + "\nSana: " + appointment["date"]
        await update.message.reply_text(msg)
    else:
        msg = "Format notogri!\nQuyidagicha yozing:\nIsm: Aliyev Vohid\nSoat: 14:30\nSana: 29.05.2026"
        await update.message.reply_text(msg)

async def get_appointments(update: Update, context: ContextTypes.DEFAULT_TYPE):
    appointments = load_appointments()
    if not appointments:
        await update.message.reply_text("Navbatlar yoq")
        return
    t = "Bugungi navbatlar:\n"
    for i, a in enumerate(appointments, 1):
        t += str(i) + ". " + a["name"] + " - " + a["time"] + " (" + a["date"] + ")\n"
    await update.message.reply_text(t)

async def clear_appointments(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_appointments([])
    await update.message.reply_text("Barcha navbatlar tozalandi!")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("navbatlar", get_appointments))
    app.add_handler(CommandHandler("tozala", clear_appointments))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
