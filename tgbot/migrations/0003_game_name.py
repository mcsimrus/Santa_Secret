# Generated by Django 3.2.9 on 2021-12-16 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0002_alter_gameparticipant_recipient'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='name',
            field=models.CharField(max_length=50, null=True, verbose_name='название игры'),
        ),
    ]