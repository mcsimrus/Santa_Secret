import sys
import logging
from typing import Dict

from telegram import Bot, BotCommand
from telegram.ext import (
    ConversationHandler, Updater,
    Dispatcher, Filters,
    CommandHandler, MessageHandler,
)
import telegram.error

from datetime import datetime, timezone, timedelta

from santa_secret.settings import TELEGRAM_TOKEN, DEBUG
from tgbot.handlers import main_handlers, user_handlers, game_handlers
from tgbot.models import Game


MOSCOW_TIMEZONE = timezone(timedelta(hours=3))


def send_messages_to_ended_games(send_hour, send_timezone: timezone):
    now = datetime.now(send_timezone)
    hour = now.hour
    if hour == send_hour:
        games = Game.objects.filter(send_date=now.date()).filter(is_ended=False)
        for game in games:
            if game.participants.filter(recipient=None):
                game.calculate_recipients_in_game()

            for participant in game.participants:
                # send_message here
                pass
            game.is_ended = True
            game.save()


main_handler = ConversationHandler(
    entry_points=[
        CommandHandler('start', main_handlers.start),
        # MessageHandler(Filters.regex('^Начать$'), main_handlers.start)
    ],
    states={
        # user branch
        main_handlers.DO_USER: [
            MessageHandler(Filters.regex('^Приступить к регистрации$'),
                           user_handlers.get_name)
        ],
        user_handlers.GET_NAME: [
            MessageHandler(Filters.text, user_handlers.get_email)
        ],
        user_handlers.GET_EMAIL: [
            MessageHandler(Filters.text, user_handlers.get_wish_list)
        ],
        user_handlers.GET_WISH_LIST: [
            MessageHandler(Filters.text, user_handlers.get_santa_letter)
        ],
        user_handlers.GET_SANTA_LETTER: [
            MessageHandler(Filters.text, user_handlers.end_registration)
        ],

        main_handlers.DO_CREATE_GAME: [
            MessageHandler(Filters.regex('^Создать игру$'),
                           game_handlers.get_game_name)
        ],
        game_handlers.DO_GET_NAME: [
            MessageHandler(Filters.text, game_handlers.get_game_price_limit)
        ],
        game_handlers.DO_GET_PRICE_LIMIT: [
            MessageHandler(Filters.text, game_handlers.get_game_reg_period)
        ],
        game_handlers.DO_GET_REG_PERIOD: [
            MessageHandler(Filters.text, game_handlers.get_game_date_send)
        ],
        game_handlers.DO_GET_DATE_SEND: [
            MessageHandler(Filters.text, game_handlers.game_created)
        ],
    },
    fallbacks=[
        CommandHandler('start', main_handlers.start),
        MessageHandler(Filters.regex('^Начать$'), main_handlers.start)
    ],
    per_chat=False
)


def setup_dispatcher(dp):

    dp.add_handler(main_handler)

    return dp


def run_pooling():
    """ Run bot in pooling mode """
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    dp = updater.dispatcher
    dp = setup_dispatcher(dp)

    bot_info = Bot(TELEGRAM_TOKEN).get_me()
    bot_link = f'https://t.me/{bot_info["username"]}'

    print(f"Pooling of '{bot_link}' started")
    # it is really useful to send '👋' emoji to developer
    # when you run local test
    # bot.send_message(text='👋', chat_id=<YOUR TELEGRAM ID>)

    updater.start_polling()
    updater.idle()


bot = Bot(TELEGRAM_TOKEN)
try:
    TELEGRAM_BOT_USERNAME = bot.get_me()["username"]
except telegram.error.Unauthorized:
    logging.error(f"Invalid TELEGRAM_TOKEN.")
    sys.exit(1)


def set_up_commands(bot_instance: Bot) -> None:
    langs_with_commands: Dict[str, Dict[str, str]] = {
        'ru': {
            'start': 'Начать пользоваться ботом'
        }
    }

    bot_instance.delete_my_commands()
    for language_code in langs_with_commands:
        bot_instance.set_my_commands(
            language_code=language_code,
            commands=[
                BotCommand(command, description) for command, description in
                langs_with_commands[language_code].items()
            ]
        )


# WARNING: it's better to comment the line below in DEBUG mode.
# Likely, you'll get a flood limit control error, when restarting bot too often
set_up_commands(bot)

n_workers = 1 if DEBUG else 4
dispatcher = setup_dispatcher(
    Dispatcher(bot, update_queue=None, workers=n_workers, use_context=True)
)
