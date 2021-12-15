import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'santa_secret.settings')
django.setup()

from tgbot.dispatcher import run_pooling

if __name__ == "__main__":
    run_pooling()
