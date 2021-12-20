from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CallbackContext, ConversationHandler
from tgbot.models import User, GameParticipant, Game

GET_NAME, GET_EMAIL, GET_WISH_LIST, GET_SANTA_LETTER = range(10, 14)


def get_name(update: Update, context: CallbackContext):
    try:
        user = User.objects.get(telegram_id=update.message.from_user['id'])
    except User.DoesNotExist:
        update.message.reply_text(
            'Введите свое имя:',
            reply_markup=ReplyKeyboardRemove()
        )
        return GET_NAME
    else:
        update.message.reply_text(
            'Вижу вы участвуете в наших играх не в первый раз.'
            ' Можем сразу переходить к списку пожеланий.'
        )
        context.user_data['model_object'] = user
        context.user_data['name'] = user.fio
        context.user_data['email'] = user.email
        return get_wish_list(update, context)


def get_email(update: Update, context: CallbackContext):
    context.user_data['name'] = update.message.text

    update.message.reply_text(
        'Введите свой адрес электронной почты:'
    )
    return GET_EMAIL


def get_wish_list(update: Update, context: CallbackContext):
    if not context.user_data.get('model_object'):
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
        context.user_data['wish_list'] = ''

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
        context.user_data['santa_letter'] = ''

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

    user_id = update.message.from_user['id']
    user_model_object = context.user_data.get('model_object')

    if not user_model_object:
        User.objects.create(
            telegram_id=user_id,
            fio=user_data['name'],
            email=user_data['email']
        )
        user_model_object = User.objects.get(telegram_id=update.message.from_user['id'])

    GameParticipant.objects.create(
        user=user_model_object,
        game=Game.objects.get(id=user_data['game_id']),
        wish_list=user_data['wish_list'],
        santa_letter=user_data['santa_letter']
    )

    return ConversationHandler.END


if __name__ == '__main__':
    print(GET_NAME, GET_EMAIL, GET_WISH_LIST, GET_SANTA_LETTER)
