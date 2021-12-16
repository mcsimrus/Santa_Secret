from telegram import Update
from telegram.ext import CallbackContext


def generate_game_link():
    """
    TODO: Функция генерации ссылки на игру для приглашения новых пользователей
    """
    pass


DO_CREATE, DO_USER = range(2)


def start(update: Update, context: CallbackContext):
    args = context.args
    if args:
        game_id = args[0]
        # do database things here
        update.message.reply_text(
            f'Привет. ID игры {game_id}'
        )
        return DO_USER
    else:
        # do pre-create things here
        update.message.reply_text(
            f'Привет. ID игры не получен'
        )
        return DO_CREATE
