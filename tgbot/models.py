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

        while True:
            is_changed = False
            for i in range(len(participants)):
                if i != len(participants) - 1:
                    sender = participants[i]
                    recipient = participants[i+1]
                    excluded_recipients = [pair.recipient for pair in sender.excluded_pair_as_sender.all()]
                    if recipient in excluded_recipients:
                        is_changed = True
                        if i+2 != len(participants):
                            participants[i+1], participants[i+2] = participants[i+2], participants[i+1]
                        else:
                            participants[i+1], participants[0] = participants[0], participants[i+1]
                else:
                    sender = participants[i]
                    recipient = participants[0]
                    excluded_recipients = [pair.recipient for pair in sender.excluded_pair_as_sender.all()]
                    if recipient in excluded_recipients:
                        is_changed = True
                        participants[0], participants[1] = participants[1], participants[0]
            if not is_changed:
                break

        for i, participant in enumerate(participants):
            if i != len(participants) - 1:
                participant.recipient = participants[i + 1]
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

    def __str__(self):
        return f'Пользователь {self.fio}'


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
        verbose_name='пользователь',
        related_name='participations'
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

    def __str__(self):
        return f'{self.user} в игре {self.game}'


class ExcludePairs(models.Model):
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        verbose_name='игра',
        related_name='excluded_pairs'
    )
    sender = models.ForeignKey(
        GameParticipant,
        on_delete=models.CASCADE,
        verbose_name='Отправитель подарка',
        related_name='excluded_pair_as_sender'
    )
    recipient = models.ForeignKey(
        GameParticipant,
        on_delete=models.CASCADE,
        verbose_name='Получатель подарка',
        related_name='excluded_pair_as_recipient'
    )

    def __str__(self):
        return f'Игра {self.game}'
