from django.utils.datetime_safe import datetime
from rest_framework import serializers
from .models import *

# Fake:

class FileSerializer(serializers.ModelSerializer):
  class Meta():
    model = File
    fields = ('file', 'timestamp')

# Reals:

class AddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Address
        fields = ('street', 'suite', 'city', 'zipcode',)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    posts = serializers.HyperlinkedRelatedField(many=True, view_name='post-detail', read_only=True)
    address = AddressSerializer(read_only=True)
    class Meta:
        model = User
        fields = ('name', 'email', 'address', 'posts',)

class UserTotalSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('pk', 'name', 'total_posts', 'total_comments',)


class ProfileInnerPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'body', 'total_comments',)

class ProfilePostSerializer(serializers.ModelSerializer):
    posts = ProfileInnerPostSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ('name', 'email', 'address', 'posts',)

class PostSerializerDetail(serializers.HyperlinkedModelSerializer):
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='name')
    comments = serializers.SlugRelatedField(many=True,read_only=True,slug_field='body')

    class Meta:
        model = Post
        fields = ('title','body', 'user', 'comments')
        
class PostSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='name')
    comments = serializers.HyperlinkedRelatedField(many=True, view_name='comment-detail', read_only=True)

    class Meta:
        model = Post
        fields = ('title','body', 'user', 'comments')

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ('name','email', 'body', 'post',)