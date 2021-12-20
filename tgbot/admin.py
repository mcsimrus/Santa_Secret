from django.contrib import admin

from .models import Game, User, GameParticipant, ExcludePairs


@admin.action(description='Устроить жеребьевку участников')
def make_recipients_in_game(modeladmin, request, queryset):
    for game in queryset:
        game.calculate_recipients_in_game()


class GameAdmin(admin.ModelAdmin):
    actions = [make_recipients_in_game]
    list_display = [
        'name', 'min_sum', 'max_sum', 'end_date', 'send_date', 'is_ended'
    ]


class UserAdmin(admin.ModelAdmin):
    list_display = [
        'telegram_id', 'fio', 'email'
    ]


class GameParticipantAdmin(admin.ModelAdmin):
    list_display = [
        'game', 'user', 'recipient', 'wish_list', 'santa_letter'
    ]


class ExcludePairsAdmin(admin.ModelAdmin):
    list_display = [
        'game', 'sender', 'recipient'
    ]


admin.site.register(Game, GameAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(GameParticipant, GameParticipantAdmin)
admin.site.register(ExcludePairs, ExcludePairsAdmin)
