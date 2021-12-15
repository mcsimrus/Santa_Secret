from datetime import date, datetime, timedelta
import os

from dateutil.relativedelta import relativedelta
from telegram import ParseMode, ShippingOption, Update, ReplyKeyboardRemove, \
    LabeledPrice
from telegram.ext import CallbackContext, ConversationHandler

from santa_secret.settings import PROVIDER_TOKEN, BASE_DIR, CONSENT_PD_FILEPATH
# from tgbot.models import ...
from tgbot.handlers.rent import static_text
# from .keyboard_utils import (
# ...
# )

from ..common.keyboard_utils import make_keyboard_for_start_command

# Список констант, по которым происходит переход после выполнения команд
# (
#     ...
# ) = range(19)
