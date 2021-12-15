from django.db import models


class Game(models.Model):
    min_sum = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='минимальная сумма'
    )
    max_sum = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='максимальная сумма'
    )
    start_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='старт приема заявок'
    )
    end_date = models.DateField(
        verbose_name='окончание приема заявок'
    )
    send_date = models.DateField(
        verbose_name='дата отправки подарков'
    )


class User(models.Model):
    telegram_id = models.IntegerField(
        primary_key=True,
        verbose_name='ID пользователя Telegram'
    )
    fio = models.CharField(
        max_length=100,
        verbose_name='ФИО'
    )
    email = models.CharField(max_length=100)


class GameParticipant(models.Model):
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        verbose_name='игра'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='пользователь'
    )
    recipient = models.ForeignKey(
        'GameParticipant',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='получатель подарка',
        related_name='sender'
    )
    wish_list = models.TextField(
        verbose_name='список желаний',
        blank=True
    )
    santa_letter = models.TextField(
        verbose_name='письмо Санте',
        blank=True
    )
