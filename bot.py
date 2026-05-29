import os
import json
import asyncio
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime

TOKEN = os.environ.get("BOT_TOKEN", "7874069508:AAG_yIIwd9Z9TRPXWMbzbeXQsH4y_36GNKc")
DATA_FILE = "/tmp/appointments.json"

def load_appointments():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_appointments(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path == "/appointments":
                result = load_appointments()
                data = json.dumps(result, ensure_ascii=False)
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(data.encode("utf-8"))
            elif self.path == "/clear":
                save_appointments([])
                self.send_response(200)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write(b"Cleared!")
            else:
                self.send_response(200)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write("Bot ishlayapti!".encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode("utf-8"))

    def log_message(self, format, *args):
        pass

def run_http_server():
    port = int(os.environ.get("PORT", 8080))
    print(f"HTTP server port: {port}", flush=True)
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()

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

async def clear_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_appointments([])
    await update.message.reply_text("Barcha navbatlar tozalandi!")

async def run_bot():
    print("Bot starting...", flush=True)
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("navbatlar", get_appointments))
    app.add_handler(CommandHandler("tozala", clear_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    await app.initialize()
    await app.start()
    await app.updater.start_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True
    )
    print("Bot started successfully!", flush=True)
    await asyncio.Event().wait()

def main():
    http_thread = threading.Thread(target=run_http_server, daemon=True)
    http_thread.start()
    print("Starting bot...", flush=True)
    asyncio.run(run_bot())

if __name__ == "__main__":
    main()
