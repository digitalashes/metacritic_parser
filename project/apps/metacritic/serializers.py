from rest_framework import serializers

from metacritic.models import Game


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('title', 'score')
