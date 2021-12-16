from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext


def generate_game_link():
    """
    TODO: Функция генерации ссылки на игру для приглашения новых пользователей
    """
    pass


DO_CREATE, DO_USER = range(2)


def start(update: Update, context: CallbackContext):
    keyboard = [
        [
            'Приступить'
        ]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    args = context.args
    if args:
        game_id = args[0]
        update.message.reply_text(
            f'Привет. ID игры {game_id}. Это временное сообщение, в будущем здесь будет информация об игре. '
            f'Нажми на кнопку ниже, чтобы перейти к заполнению данных',
            reply_markup=reply_markup
        )
        return DO_USER
    else:
        # do pre-create things here
        update.message.reply_text(
            f'Привет. ID игры не получен'
        )
        return DO_CREATE
