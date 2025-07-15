# bot.py

import os
from dotenv import load_dotenv
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

# Load your bot token securely from the .env file
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# --- /start Command ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello, human. I'm your bot.")

# --- /help Command ---
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🛠️ Here are the available commands:\n"
        "/start – Start the bot\n"
        "/help – Show this help message\n"
        "/echo <text> – Echoes what you send\n"
        "/menu – Show reply keyboard buttons\n"
        "/inline – Show inline buttons\n"
    )
    await update.message.reply_text(help_text)

# --- /echo Command ---
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        user_message = " ".join(context.args)
        await update.message.reply_text(f"🗣️ {user_message}")
    else:
        await update.message.reply_text("You didn’t say anything after /echo!")

# --- /menu Command: Reply Keyboard ---
async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    menu_keyboard = [
        ["/start", "/help"],
        ["/echo Hello!", "Get Quote"]
    ]
    markup = ReplyKeyboardMarkup(menu_keyboard, resize_keyboard=True)
    await update.message.reply_text("Choose an option:", reply_markup=markup)

# --- /inline Command: Inline Buttons ---
async def inline_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [
            InlineKeyboardButton("Google 🌐", url="https://google.com"),
            InlineKeyboardButton("Refresh 🔁", callback_data="refresh")
        ]
    ]
    markup = InlineKeyboardMarkup(buttons)
    await update.message.reply_text("Click a button below:", reply_markup=markup)

# --- Callback for Inline Buttons ---
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "refresh":
        await query.edit_message_text("🔁 You clicked Refresh!")

# --- Main Application Setup ---
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("echo", echo))
    app.add_handler(CommandHandler("menu", show_menu))
    app.add_handler(CommandHandler("inline", inline_buttons))

    # Callback handler for inline button clicks
    app.add_handler(CallbackQueryHandler(handle_callback))

    app.run_polling()

if __name__ == "__main__":
    main()
