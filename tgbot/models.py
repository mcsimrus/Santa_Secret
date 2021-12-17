from django.db import models
from random import shuffle


class Game(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='название игры'
    )
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
    end_date = models.DateField(
        verbose_name='окончание приема заявок'
    )
    send_date = models.DateField(
        verbose_name='дата отправки подарков'
    )

    def game_id(self):
        return f'{self.id}-{self.name}'

    def __str__(self):
        return self.game_id()

    def calculate_recipients_in_game(self):
        participants = list(self.participants.all())
        shuffle(participants)
        for i, participant in enumerate(participants):
            if i != len(participants) - 1:
                participant.recipient = participants[i+1]
            else:
                participant.recipient = participants[0]

            participant.save()


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
        verbose_name='игра',
        related_name='participants'
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
