from django.conf import settings
from rest_framework.filters import OrderingFilter
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import get_object_or_404

from metacritic.models import Game
from metacritic.models import Platform
from metacritic.serializers import GameSerializer


class GameListApiView(ListAPIView):
    filter_backends = (OrderingFilter, SearchFilter)
    ordering = ('title', 'score')
    queryset = Game.objects.select_related(
        'platform'
    ).filter(
        platform=Platform.objects.get(name=settings.DEFAULT_PLATFORM)
    )
    search_fields = ('title',)
    serializer_class = GameSerializer


class GameRetrieveApiView(RetrieveAPIView):
    lookup_field = 'title'
    queryset = Game.objects.select_related(
        'platform'
    ).filter(
        platform=Platform.objects.get(name=settings.DEFAULT_PLATFORM)
    )
    serializer_class = GameSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

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
