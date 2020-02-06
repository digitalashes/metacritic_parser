from rest_framework import serializers

from metacritic.models import Game
from metacritic.models import Platform


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ('id', 'name')


class GameSerializer(serializers.ModelSerializer):
    platform = PlatformSerializer()

    class Meta:
        model = Game
        fields = ('id', 'title', 'score', 'platform')
