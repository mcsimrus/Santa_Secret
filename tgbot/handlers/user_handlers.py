from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CallbackContext, ConversationHandler

GET_NAME, GET_EMAIL, GET_WISH_LIST, GET_SANTA_LETTER = range(10, 14)


def get_name(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Введите свое имя:'
    )
    return GET_NAME


def get_email(update: Update, context: CallbackContext):
    context.user_data['name'] = update.message.text

    update.message.reply_text(
        'Введите свой адрес электронной почты:'
    )
    return GET_EMAIL


def get_wish_list(update: Update, context: CallbackContext):
    context.user_data['email'] = update.message.text

    keyboard = [
        [
            'Пропустить'
        ]
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard, resize_keyboard=True
    )

    update.message.reply_text(
        'Введите список пожеланий или нажмите на кнопку пропустить',
        reply_markup=reply_markup
    )

    return GET_WISH_LIST


def get_santa_letter(update: Update, context: CallbackContext):
    if update.message.text != 'Пропустить':
        context.user_data['wish_list'] = update.message.text
    else:
        context.user_data['wish_list'] = None

    keyboard = [
        [
            'Пропустить'
        ]
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard, resize_keyboard=True
    )

    update.message.reply_text(
        'Введите письмо Санте или нажмите на кнопку пропустить',
        reply_markup=reply_markup
    )

    return GET_SANTA_LETTER


def end_registration(update: Update, context: CallbackContext):
    if update.message.text != 'Пропустить':
        context.user_data['santa_letter'] = update.message.text
    else:
        context.user_data['santa_letter'] = None

    update.message.reply_text(
        'Превосходно, ты в игре! 31.12.2021 мы проведем жеребьёвку '
        'и ты узнаешь имя и контакты своего тайного друга. '
        'Ему и нужно будет подарить подарок!',
        reply_markup=ReplyKeyboardRemove()
    )

    user_data = context.user_data

    user_data_message = (f'Имя: {user_data["name"]}\n'
                         f'Email: {user_data["email"]}\n'
                         f'Вишлист: {user_data["wish_list"]}\n'
                         f'Письмо Санте: {user_data["santa_letter"]}')

    update.message.reply_text(user_data_message)

    # here be database things

    return ConversationHandler.END


if __name__ == '__main__':
    print(GET_NAME, GET_EMAIL, GET_WISH_LIST, GET_SANTA_LETTER)
