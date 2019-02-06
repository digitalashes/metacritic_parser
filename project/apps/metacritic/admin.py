from django.contrib import admin

from metacritic.models import Game
from metacritic.models import Platform


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'score', 'platform')
    list_display_links = ('title',)
    list_filter = ('platform',)
    list_select_related = ('platform',)
    raw_id_fields = ('platform',)
    readonly_fields = ('created', 'modified')
    search_fields = ('title', 'score', 'platform')
