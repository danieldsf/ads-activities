from drf_enum_field.serializers import EnumFieldSerializerMixin
from rest_framework import serializers
from core.models import *

class DishRatingSerializer(EnumFieldSerializerMixin, serializers.HyperlinkedModelSerializer):
    owner = serializers.SlugRelatedField(queryset=PersonProfile.objects.all(), slug_field='fullname')
    dish = serializers.SlugRelatedField(queryset=Dish.objects.all(), slug_field='name')

    class Meta:
        model = DishRating
        fields = ('stars','comment','owner','dish')


class RestaurantRatingSerializer(EnumFieldSerializerMixin, serializers.HyperlinkedModelSerializer):
    owner = serializers.SlugRelatedField(queryset=PersonProfile.objects.all(), slug_field='fullname')
    restaurant = serializers.SlugRelatedField(queryset=Restaurant.objects.all(), slug_field='name')

    class Meta:
        model = RestaurantRating
        fields = ('stars', 'comment', 'owner', 'restaurant')

class UserSerializer(EnumFieldSerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id','username','fullname','phone','gender',)

class PostUserSerializer(EnumFieldSerializerMixin, serializers.ModelSerializer):

    def create(self, validated_data):
        obj = User.objects.create(**validated_data)
        obj.set_password(obj.password)
        obj.user_type=UserType.CLIENTE
        obj.save()
        return obj

    class Meta:
        model = User
        fields = ('username','password','fullname','phone','gender')

class UserRestaurantSerializer(EnumFieldSerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = RestaurantProfile
        fields = ('id','username','fullname','phone','gender','count_restaurants')

class PostUserRestaurantSerializer(EnumFieldSerializerMixin, serializers.ModelSerializer):

    def create(self, validated_data):
        obj = User.objects.create(**validated_data)
        obj.set_password(obj.password)
        obj.user_type=UserType.RESTAURANTE
        obj.save()
        return obj

    class Meta:
        model = RestaurantProfile
        fields = ('username','password','fullname','phone','gender','count_restaurants')


class RestaurantSerializer(EnumFieldSerializerMixin, serializers.HyperlinkedModelSerializer):
    owner = serializers.SlugRelatedField(queryset=RestaurantProfile.objects.all(), slug_field='fullname')

    class Meta:
        model = Restaurant
        fields = ('name', 'phone', 'description',  'email','rating', 'owner')


class PostRestaurantSerializer(EnumFieldSerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = ('name', 'phone', 'description',  'email','rating', 'owner')

class DishSerializer(EnumFieldSerializerMixin, serializers.HyperlinkedModelSerializer):
    owner = serializers.SlugRelatedField(queryset=Restaurant.objects.all(), slug_field='name')

    class Meta:
        model = Dish
        fields = ('name', 'description', 'price', 'owner','rating')

class DishSerializerDetailed(EnumFieldSerializerMixin, serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(queryset=Restaurant.objects.all(), slug_field='name')
    dish_ratings = DishRatingSerializer(many=True, read_only=True)

    class Meta:
        model = Dish
        fields = ('name', 'description', 'price', 'owner', 'rating', 'dish_ratings')

class OrderSerializer(EnumFieldSerializerMixin, serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(queryset=PersonProfile.objects.all(), slug_field='fullname')
    dish_order = DishSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('name', 'owner', 'status', 'dish_order')
