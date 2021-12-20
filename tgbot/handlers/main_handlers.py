import datetime
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CallbackContext, Filters, ConversationHandler

from tgbot.models import Game
STOP_GAME_REG_HOUR = 12  # Час суток, когда заканчивается регистрация на игру

DO_CREATE_GAME, DO_USER = range(2)


def start(update: Update, context: CallbackContext):
    args = context.args
    if args:
        keyboard = [
            [
                'Приступить к регистрации'
            ]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

        game_id = args[0]
        game = Game.objects.get(id=game_id)
        context.user_data['game_id'] = game_id

        # Проверка - открыта ли ещё регистрация на игру
        if datetime.date.today() >= game.end_date \
                and datetime.datetime.today().hour >= STOP_GAME_REG_HOUR:
            update.message.reply_text(
                f'К сожалению, регистрация участников на игру "{game.name}"'
                f' завершилась {game.end_date.strftime("%d.%m.%Y")} в'
                f' {STOP_GAME_REG_HOUR} часов.\n'
                'С наступающим вас Новым Годом!!!',
                reply_markup=ReplyKeyboardRemove()
            )
            return ConversationHandler.END

        message = (f'Замечательно, ты собираешься участвовать в игре:\n'
                   f'Название игры: {game.name}\n'
                   f'Дата окончания регистрации: {game.end_date}\n'
                   'Минимальная стоимость подарка:'
                   f' {game.min_sum if game.min_sum else "Отсутствует"}\n'
                   'Максимальная стоимость подарка:'
                   f' {game.max_sum if game.max_sum else "Отсутствует"}\n'
                   f'Дата отправки подарков: {game.send_date}')

        update.message.reply_text(
            message
        )

        update.message.reply_text(
            'Нажми на кнопку "Приступить к регистрации", чтобы перейти к'
            ' регистрации в игре',
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

