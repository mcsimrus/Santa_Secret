from datetime import date
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CallbackContext, ConversationHandler

from tgbot.models import Game
from datetime import timezone, datetime

DO_GET_NAME, DO_GET_PRICE_LIMIT, DO_GET_REG_PERIOD, DO_GET_DATE_SEND, \
    DO_GAME_CREATED = range(50, 55)

GAME_PRICE_LIMITS = [
    'нет',
    'до 500 рублей',
    '500-1000 рублей',
    '1000-2000 рублей'
]

GAME_REG_PERIODS = ['до 25.12.2021', 'до 31.12.2021']

GET_DATE_MSG = 'Введите дату отправки подарка (ДД.ММ.ГГГГ):'


def generate_game_link(update, context):
    return f'https://t.me/{context.bot.username}' \
           f'?start={context.user_data["game_id"]}'


def show_context_user_data(fn_name, context_user_data):
    print(f'context_user_data - {fn_name}: {context_user_data}')


def get_game_name(update: Update, context: CallbackContext):
    # from DO_CREATE_GAME
    update.message.reply_text(
        'Введите название игры:',
        reply_markup=ReplyKeyboardRemove()
    )
    show_context_user_data('get_game_name', context.user_data)
    return DO_GET_NAME


def get_game_price_limit(update: Update, context: CallbackContext):
    # from DO_GET_NAME
    context.user_data['game_name'] = update.message.text

    keyboard = [
        GAME_PRICE_LIMITS
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard, resize_keyboard=True
    )

    update.message.reply_text(
        'Выберите ограничение по стоимости подарка:',
        reply_markup=reply_markup
    )
    show_context_user_data('get_game_price_limit', context.user_data)
    return DO_GET_PRICE_LIMIT


def get_game_reg_period(update: Update, context: CallbackContext):
    # from DO_GET_PRICE_LIMIT
    context.user_data['game_price_limit'] = update.message.text

    keyboard = [
        GAME_REG_PERIODS
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard, resize_keyboard=True
    )

    update.message.reply_text(
        'Выберите период регистрации участников:',
        reply_markup=reply_markup
    )
    show_context_user_data('get_game_reg_period', context.user_data)
    return DO_GET_REG_PERIOD


def get_game_date_send(update: Update, context: CallbackContext):
    # from DO_GET_REG_PERIOD
    context.user_data['game_reg_period'] = update.message.text

    update.message.reply_text(
        text=GET_DATE_MSG,
        reply_markup=ReplyKeyboardRemove()
    )
    show_context_user_data('get_game_date_send', context.user_data)
    return DO_GET_DATE_SEND


def game_created(update: Update, context: CallbackContext):
    # from DO_GET_DATE_SEND
    value = update.message.text.replace(',', '.')
    try:
        day, month, year = value.split('.')
        if len(day) > 2 or len(month) > 2 or len(year) != 4:
            raise ValueError
        day, month, year = map(int, (day, month, year))
        send_date = date(year, month, day)
    except ValueError:
        update.message.reply_text(
            text=f'Ошибка! "{value}" не является корректной датой.'
        )
        return get_game_date_send(update, context)

    if send_date < date.today():
        update.message.reply_text(
            text=f'Введённая дата отправки подарков "{value}'
                 '" должна быть больше текущей!'
        )
        return get_game_date_send(update, context)

    context.user_data['game_date_send'] = update.message.text

    min_sum = 0
    max_sum = 0
    if context.user_data['game_price_limit'] == GAME_PRICE_LIMITS[0]:
        min_sum = 0
        max_sum = 0
    elif context.user_data['game_price_limit'] == GAME_PRICE_LIMITS[1]:
        min_sum = 0
        max_sum = 500
    elif context.user_data['game_price_limit'] == GAME_PRICE_LIMITS[2]:
        min_sum = 500
        max_sum = 1000
    elif context.user_data['game_price_limit'] == GAME_PRICE_LIMITS[3]:
        min_sum = 1000
        max_sum = 2000

    if context.user_data['game_reg_period'] == GAME_REG_PERIODS[0]:
        date_to = date(2021, 12, 25)
    else:
        date_to = date(2021, 12, 31)

    game = Game(
        name=context.user_data['game_name'],
        min_sum=min_sum,
        max_sum=max_sum,
        end_date=date_to,
        send_date=send_date
    )
    game.save()
    context.user_data['game_id'] = game.id

    game_url = generate_game_link(update, context)

    update.message.reply_text(
        text='Отлично, Тайный Санта уже готовится к раздаче подарков!\n' +
             game_url
    )
    show_context_user_data('game_created', context.user_data)
    return ConversationHandler.END


# if __name__ == '__main__':
#     print(GAME_PRICE_LIMITS[0])
