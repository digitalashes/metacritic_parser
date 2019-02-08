from django.contrib import admin
from django.urls import path

from metacritic.models import Game
from metacritic.models import Platform
from metacritic.views import ParserViewForm


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'score', 'platform', 'created', 'modified')
    list_display_links = ('title',)
    list_filter = ('platform',)
    list_select_related = ('platform',)
    ordering = ('-score', 'title')
    raw_id_fields = ('platform',)
    readonly_fields = ('created', 'modified')
    search_fields = ('title', 'score',)
    change_list_template = 'change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        additional_urls = [
            path('parse',
                 self.admin_site.admin_view(self.parse_conf),
                 name='metacritic_game_parse'),
        ]
        return urls + additional_urls

    @staticmethod
    def parse_conf(request):
        return ParserViewForm.as_view()(request)
