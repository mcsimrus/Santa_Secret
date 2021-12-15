from telegram import ParseMode, Update
from telegram.ext import ConversationHandler

# from tgbot.models import ...
from tgbot.handlers.common import static_text
from .keyboard_utils import make_keyboard_for_start_command


def command_start(update: Update, _):
    user_info = update.message.from_user.to_dict()
    msg_text = static_text.start_new_game.format(
        first_name=user_info['first_name']
    )

    update.message.reply_text(
        text=msg_text,
        reply_markup=make_keyboard_for_start_command(),
    )


def command_cancel(update: Update, _):
    text = 'Отмена'
    update.message.reply_text(
        text=text,
        reply_markup=make_keyboard_for_start_command(),
    )
    return ConversationHandler.END
