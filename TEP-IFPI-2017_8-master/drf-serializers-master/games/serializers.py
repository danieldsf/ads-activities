from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Game
from django.db import models

class GameSerializer(serializers.ModelSerializer):
    
    class Meta():
        model = Game
        fields = ('id', 'name', 'release_date', 'game_category')
        '''
        name = models.CharField(
            validators=[UniqueValidator(queryset=Game.objects.all())]
        )
        '''
