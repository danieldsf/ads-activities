"""
Book: Building RESTful Python Web Services
Chapter 2: Working with class based views and hyperlinked APIs in Django
Author: Gaston C. Hillar - Twitter.com/gastonhillar
Publisher: Packt Publishing Ltd. - http://www.packtpub.com
"""
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from .models import Game
from .serializers import GameSerializer
from .utils import *

@api_view(['GET', 'POST'])
def game_list(request):
    if request.method == 'GET':
        games = Game.objects.all()
        games_serializer = GameSerializer(games, many=True)
        return Response(games_serializer.data)
    elif request.method == 'POST':
        game_serializer = GameSerializer(data=request.data)
        
        # Null

        feedback = check_valid_list(game_serializer.initial_data, ('name', 'release_date', 'game_category'))
        
        if feedback:
            return Response({'errors': feedback}, status=status.HTTP_400_BAD_REQUEST)

        # Nome Unique:
        if check_unique(Game, game_serializer.initial_data['name']):
            return Response({'errors': [{'name': 'Nome ja utilizado'}]}, status=status.HTTP_400_BAD_REQUEST)


        if game_serializer.is_valid():
            game_serializer.save()
            return Response(game_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(game_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE' ])
def game_detail(request, pk):
    try:
        game = Game.objects.get(pk=pk)
    except Game.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        game_serializer = GameSerializer(game)
        return Response(game_serializer.data)
        
    elif request.method == "PUT":
        game_serializer = GameSerializer(game, data=request.data)
        if game_serializer.is_valid():
            game_serializer.save()
            return Response(game_serializer.data)
        return Response(game_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        if game.release_date <= timezone.now():
            game.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': {'release_date': 'Game nao lancado'}}, status=status.HTTP_409_CONFLICT)
