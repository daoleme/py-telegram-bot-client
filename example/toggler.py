"""
run in cli: python -m example.toggler.py
"""
import logging
from simplebot import bot_proxy, SimpleBot
from simplebot.base import (
    CallbackQuery,
    InlineKeyboardButton,
    Message,
    MessageField,
)
from simplebot.ui import InlineKeyboard
from example.settings import BOT_TOKEN

logger = logging.getLogger("simple-bot")
logger.setLevel(logging.DEBUG)

router = bot_proxy.router()
example_bot = bot_proxy.create_bot(token=BOT_TOKEN, router=router)
example_bot.delete_webhook(drop_pending_updates=True)


def toggle_on_callback(bot: SimpleBot, callback_query: CallbackQuery):
    print("toggler is on")


def toggle_off_callback(bot: SimpleBot, callback_query: CallbackQuery):
    print("toggler is off")


InlineKeyboard.set_toggle_callback(
    router,
    name="toggler",
    toggle_on_callback=toggle_on_callback,
    toggle_off_callback=toggle_off_callback,
)


@router.message_handler(fields=(MessageField.TEXT,))
def on_show_keyboard(bot: SimpleBot, message: Message):
    keyboard = InlineKeyboard()
    keyboard.add_toggler("toggler", checked=True)
    keyboard.add_buttons(InlineKeyboardButton(text="submit", callback_data="submit"))
    bot.send_message(
        chat_id=message.chat.id, text="Your selections:", reply_markup=keyboard.markup()
    )


@router.callback_query_handler(static_match="submit")
def on_submit(bot, callback_query):
    keyboard = InlineKeyboard(markup=callback_query.message.reply_markup)
    bot.send_message(
        chat_id=callback_query.from_user.id,
        text="you select: {0}".format(keyboard.get_toggler_status("toggler")),
    )


example_bot.run_polling(timeout=10)
