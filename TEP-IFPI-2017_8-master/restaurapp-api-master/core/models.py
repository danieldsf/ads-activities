from django.db import models
from django.contrib.auth.models import AbstractUser
from enumfields import EnumField
from .enums import *
from .managers import *

class User(AbstractUser):
    objects = CaseInsensitiveUserManager()
    fullname = models.CharField(max_length=50, null=False)
    phone = models.CharField(max_length=11, null=True, unique=False, default="86899936097")
    gender = EnumField(Gender, default=Gender.OUTRO)
    user_type = EnumField(UserType, default=UserType.CLIENTE)

    class Meta:
        ordering=('fullname',)

    @property
    def count_orders(self):
        return self.orders.count

    @property
    def get_gender(self):
        if self.gender==Gender.MASCULINO:
            return "MASCULINO"
        elif self.gender==Gender.FEMININO:
            return "FEMININO"
        return "OUTRO"

    @property
    def get_user_type(self):
        if self.user_type == UserType.CLIENTE:
            return "CLIENTE"
        return "RESTAURANTE"

    def __str__(self):
        return self.fullname


class PersonProfile(User):
    
    objects = PersonProfileManager()

    class Meta:
        proxy = True

    @property
    def get_name(self):
        return self.fullname

    def create(self, **kwargs):
        kwargs.update({'user_type': UserType.CLIENTE})
        return super(PersonProfile, self).create(**kwargs)


class RestaurantProfile(User):
    
    objects = RestaurantProfileManager()

    class Meta:
        proxy = True

    @property
    def count_restaurants(self):
        return self.restaurants.count()
    
    def create(self, **kwargs):
        kwargs.update({'user_type': UserType.RESTAURANTE})
        return super(RestaurantProfile, self).create(**kwargs)

class Restaurant(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)
    phone = models.CharField(max_length=11, null=False, unique=True)
    description = models.CharField(max_length=11, null=False)
    owner = models.ForeignKey(RestaurantProfile, on_delete=models.CASCADE, related_name="restaurants", null=False)
    email = models.CharField(max_length=50, null=False, unique=True)
    adress = models.CharField(max_length=100, null=False)

    class Meta:
        ordering=('name',)

    def __str__(self):
        return self.name

    @property
    def rating(self):
        sum = 0
        count = 0
        for i in self.restaurant_ratings.all():
            sum+=i.stars
            count+=1
        if count == 0:
            count = 1
        return sum/count


class Dish(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    description = models.CharField(max_length=400, null=False)
    price = models.FloatField(null=False, default=0)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="dishes", null=False)

    class Meta:
        ordering=('name',)

    def __str__(self):
        return self.name

    @property
    def rating(self):
        sum = 0
        count = 0
        for i in self.dish_ratings.all():
            sum += i.stars
            count += 1
        if count == 0:
            count = 1
        return sum/count

    @property
    def dish_ratings(self):
        return self.dish_ratings

class Order(models.Model):
    name = models.CharField(max_length=40, null=False)
    owner = models.ForeignKey(PersonProfile, on_delete=models.CASCADE, related_name="orders", null=False)
    created = models.DateTimeField(auto_now_add=True)
    status = EnumField(OrderStatus, default=OrderStatus.RECEBIDO)
    dish_order = models.ManyToManyField(Dish, related_name="orders")

    class Meta:
        ordering=('name',)

    def __str__(self):
        return self.name

class DishRating(models.Model):
    stars = models.IntegerField(null=False, default=5)
    comment = models.CharField(max_length=100, null=False)
    owner = models.ForeignKey(PersonProfile, on_delete=models.CASCADE, related_name="dish_ratings", null=False)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name="dish_ratings", null=False)

    class Meta:
        ordering=('stars',)

    def __str__(self):
        return self.comment

class RestaurantRating(models.Model):
    stars = models.IntegerField(null=False, default=5)
    comment = models.TextField(null=False)
    owner = models.ForeignKey(PersonProfile, on_delete=models.CASCADE, related_name="restaurant_ratings", null=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="restaurant_ratings", null=False)

    class Meta:
        ordering=('stars',)

    def __str__(self):
        return self.comment