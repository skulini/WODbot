import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext
import db

TOKEN = os.getenv(7946610248:AAGArla71L_EfKtl1zP11Wn83t4yqODEsmY)
db.init_db()

async def start(update: Update, context: CallbackContext):
    keyboard = [["/add", "/wod"], ["/inventory", "/myinv"]]
    await update.message.reply_text(
        "Привет! Я твой CrossFit бот 💪\n"
        "Команды:\n"
        "/add <текст> – добавить тренировку\n"
        "/wod – случайная тренировка\n"
        "/inventory <список> – задать инвентарь\n"
        "/myinv – показать твой инвентарь",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

async def add(update: Update, context: CallbackContext):
    text = " ".join(context.args)
    if not text:
        await update.message.reply_text("Напиши: /add <описание тренировки>")
        return
    db.add_workout(text, "manual")
    await update.message.reply_text("Тренировка сохранена ✅")

async def wod(update: Update, context: CallbackContext):
    workout = db.get_random_workout()
    await update.message.reply_text(f"🔥 Тренировка:\n{workout}")

async def inventory(update: Update, context: CallbackContext):
    text = " ".join(context.args)
    if not text:
        await update.message.reply_text("Напиши: /inventory гантели, турник, мяч")
        return
    db.set_inventory(update.message.from_user.id, text)
    await update.message.reply_text("Инвентарь сохранён ✅")

async def myinv(update: Update, context: CallbackContext):
    inv = db.get_inventory(update.message.from_user.id)
    await update.message.reply_text(f"Твой инвентарь: {inv}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("wod", wod))
    app.add_handler(CommandHandler("inventory", inventory))
    app.add_handler(CommandHandler("myinv", myinv))
    app.run_polling()

if __name__ == "__main__":
    main()
