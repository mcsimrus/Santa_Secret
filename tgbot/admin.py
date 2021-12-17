from django.contrib import admin

from .models import Game, User, GameParticipant


@admin.action(description='Устроить жеребьевку участников')
def make_recipients_in_game(modeladmin, request, queryset):
    for game in queryset:
        game.calculate_recipients_in_game()


class GameAdmin(admin.ModelAdmin):
    actions = [make_recipients_in_game]


admin.site.register(Game, GameAdmin)
admin.site.register(User)
admin.site.register(GameParticipant)
