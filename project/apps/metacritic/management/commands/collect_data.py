from typing import Any
from typing import Dict
from typing import Optional
from typing import Tuple
from urllib.parse import urlparse
from urllib.parse import urlunparse

import lxml.html as lxmlhtml
import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy as _

from metacritic.models import Game
from metacritic.models import Platform

DEFAULT_URL = settings.PARSER_DEFAULT_PARSING_URL.format(platform=settings.PARSER_DEFAULT_PLATFORM)


class Command(BaseCommand):
    help = "Collect data about games"
    url = None
    headers = None
    platform = None
    data = []

    def add_arguments(self, parser):
        parser.add_argument(
            '-u',
            '--url',
            type=str,
            default=DEFAULT_URL,
            help=_('Url for parsing.')
        )

    def handle(self, *args: Tuple[Any], **options: Dict[str, Any]) -> None:
        self.check_url(options['url'] or DEFAULT_URL)

        with requests.Session() as session:
            self.fetch(session, self.url)

        if self.data:
            self.save()

    def check_url(self, url: str) -> None:
        self.stdout.write(f'\nGot {url} url\nTrying to check it.\n\n')

        parse_result = urlparse(url)
        assert parse_result.scheme == 'https', 'Incorrect scheme'
        assert parse_result.netloc == 'www.metacritic.com', 'Incorrect site hostname'
        try:
            platform = parse_result.path.split('/')[5].lower()
            assert platform in settings.PARSER_AVAILABLE_PLATFORMS, 'Incorrect platform'
        except (IndexError, AttributeError):
            raise AssertionError('Incorrect platform')
        else:
            platform, *__ = Platform.objects.get_or_create(name=platform)
            self.platform = platform
            self.stdout.write(f'Found platform. Platform name is {platform}')
        self.stdout.write('Looks like passed url is fine.\n\n')
        self.url = urlunparse((parse_result.scheme,
                               parse_result.netloc,
                               parse_result.path, '',
                               'view=condensed', ''))

    def fetch(self, session: requests.Session, url: str) -> None:
        self.stdout.write(f'Fetching games info from url - {url}')
        response = session.get(url, headers=settings.PARSER_DEFAULTS_HEADERS)
        if response.status_code != 200:
            self.stderr.write(f'Bad url - {url}\n'
                              f'Status code is {response.status_code}')
            return
        next_page = self._parse(response.content)
        if next_page:
            self.fetch(session, next_page)

    def _parse(self, html) -> Optional[str]:
        self.stdout.write('Parsing html.')
        body = lxmlhtml.fromstring(html)
        products = body.find_class('product game_product')
        self.stdout.write(f'Found {len(products)} products(s).')
        for product in products:
            title = next(
                product.find_class('basic_stat product_title')[0].iterlinks()
            )[0].text.strip()
            score = product.find_class('metascore_w')[0].text
            self.data.append({'title': title, 'score': score})
        try:
            self.stdout.write('Trying to get next url.\n\n')
            path = next(body.find_class('flipper next')[0].iterlinks())[2]
            parse_url = urlparse(self.url)
            next_url = urlunparse((parse_url.scheme, parse_url.netloc, path, '', '', ''))
            self.stdout.write(f'Got next url value. It is - {next_url}')
            return next_url
        except StopIteration:
            self.stdout.write('Looks like next url doesn\'t exists.\n'
                              'Seems it\'s a last page.\n\n')
            return None

    def save(self) -> None:
        self.stdout.write('Saving data...')

        games_qs = Game.objects.filter(platform=self.platform).values('title', 'id', 'score')
        games = {i['title']: {'id': i['id'], 'score': i['score']} for i in games_qs}
        game_for_create = []
        game_for_update = []

        for record in self.data:
            title = record['title']
            try:
                score = int(record['score'])
            except ValueError:
                self.stderr.write('Can\'t convert score %s for game %game', record['score'], record['title'])
                continue
            game = Game(platform=self.platform,
                        title=title,
                        score=score)

            game_obj = games.get(title)
            if not game_obj:
                game_for_create.append(game)
            elif game_obj['score'] != score:
                game.id = game_obj['id']
                game.score = game_obj['score']
                game_for_update.append(game)

        if game_for_create:
            Game.objects.bulk_create(game_for_create)
        if game_for_update:
            Game.objects.bulk_update(game_for_update, ['score'])

        self.stdout.write('Data has been saved.')
