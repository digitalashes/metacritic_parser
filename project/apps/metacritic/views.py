from django.conf import settings
from django.contrib import messages
from django.core.management import call_command
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from rest_framework.filters import OrderingFilter
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import get_object_or_404

from metacritic.forms import UrlForm
from metacritic.models import Game
from metacritic.models import Platform
from metacritic.serializers import GameSerializer


class ParserViewForm(FormView):  # pylint: disable=R0901
    template_name = 'parse.html'
    form_class = UrlForm
    success_url = reverse_lazy('admin:metacritic_game_changelist')

    def form_valid(self, form):
        try:
            call_command('collect_data', url=form.cleaned_data['url'])
        except Exception as e:  # pylint: disable=W0703
            messages.add_message(self.request, messages.ERROR, f'Something went wrong. {e}')
            return super().form_invalid(form)
        messages.add_message(self.request, messages.INFO, 'Data has been fetched successfully.')
        return super().form_valid(form)


class GameListApiView(ListAPIView):
    filter_backends = (
        OrderingFilter,
        SearchFilter,
    )
    ordering_fields = ('title', 'score')
    ordering = ('-score',)
    queryset = Game.objects.select_related(
        'platform'
    ).only(
        'id', 'title', 'score', 'platform'
    )
    search_fields = ('title',)
    serializer_class = GameSerializer


class GameRetrieveApiView(RetrieveAPIView):
    lookup_field = 'title'
    queryset = Game.objects.select_related(
        'platform'
    )
    serializer_class = GameSerializer

    def get_object(self):
        platform = get_object_or_404(Platform.objects, name=settings.PARSER_DEFAULT_PLATFORM)
        queryset = self.filter_queryset(
            self.get_queryset().filter(
                platform=platform
            )
        )

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {f'{self.lookup_field}__icontains': self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj


game_list = GameListApiView.as_view()
game_detail = GameRetrieveApiView.as_view()
