from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, Filters

from tgbot.models import Game
from .game_handlers import get_game_name


DO_CREATE_GAME, DO_USER = range(2)


def start(update: Update, context: CallbackContext):
    args = context.args
    if args:
        keyboard = [
            [
                'Приступить'
            ]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

        game_id = args[0]
        update.message.reply_text(
            f'Привет. ID игры {game_id}. Это временное сообщение,'
            f' в будущем здесь будет информация об игре. '
            f'Нажми на кнопку ниже, чтобы перейти к заполнению данных',
            reply_markup=reply_markup
        )
        return DO_USER
    else:
        keyboard = [
            [
                'Создать игру'
            ]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

        update.message.reply_text(
            'Организуй тайный обмен подарками, запусти праздничное настроение!',
            reply_markup=reply_markup
        )
        print(Filters.text)

        return DO_CREATE_GAME

