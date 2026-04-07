import re
import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CopyTextButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.request import HTTPXRequest

CHANNEL_USERNAME = "@Vanila_cards"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def is_user_member(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        chat_member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return chat_member.status in ("member", "administrator", "creator")
    except Exception as e:
        logger.error(f"Membership check failed for {user_id}: {e}")
        return False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_text = (
        "💠 Dear users!\n\n"
        "🚀 JOIN OUR OFFICIAL BOT FIRST!\n"
        "🤖 Buy Cards Instantly:\n"
        "👉 @vanilla_cards_bot— Type /start\n"
        "🔔 Get Instant Support:\n"
        "👉 https://t.me/Vanila_cards\n"
        "⚡ Early Join = Early Access\n"
        "🔥 Don't Miss The Best Cards!"
    )
    await update.message.reply_text(welcome_text)


async def send_card_formats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    formats = [
        "2222222222222222:22:22:222",
        "3333333333333333:33/33:333",
        "4444444444444444/44/44/444",
        "5555555555555555 55/55 555",
        "6666666666666666 66 66 666",
    ]
    keyboard = []
    for fmt in formats:
        button = InlineKeyboardButton(text=f"📋 {fmt}", copy_text=CopyTextButton(text=fmt))
        keyboard.append([button])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Welcome! Please provide your card details in a standard format:",
        reply_markup=reply_markup,
    )


CARD_PATTERN = re.compile(r'^\d{16}([:/\s])\d{2}([:/\s])\d{2}([:/\s])\d{3}$')


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_input = update.message.text.strip()
    user_id = update.effective_user.id

    if CARD_PATTERN.match(user_input):
        member = await is_user_member(user_id, context)
        if not member:
            await update.message.reply_text(
                "You can't check the card because you're not a member of @vanilla_cards_bot"
            )
        else:
            await update.message.reply_text(
                "✅ You are a member! Card details received (demo).\n"
                "Add your own card validation here."
            )
    else:
        await update.message.reply_text("❌ Invalid format")


def main() -> None:
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN environment variable is not set.")

    request = HTTPXRequest(connect_timeout=30.0, read_timeout=30.0, write_timeout=30.0, pool_timeout=30.0)
    app = Application.builder().token(bot_token).request(request).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("card_chake", send_card_formats))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot started, polling for updates...")
    app.run_polling()


if __name__ == "__main__":
    main()
