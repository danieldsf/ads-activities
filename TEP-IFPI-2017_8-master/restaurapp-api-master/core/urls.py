from django.urls import path
from .views import *

urlpatterns = [
    path('users/', UserList.as_view(), name=UserList.name),

    path('users/<int:pk>/', UserDetail.as_view(), name=UserDetail.name),
    path('users/<int:pk>/orders/', OrderList.as_view(), name=OrderList.name),
    path('users/<int:pk>/orders/<int:id>/', OrderDetail.as_view(), name=OrderDetail.name),

    path('users-restaurants/', RestaurantUserList.as_view(), name=RestaurantUserList.name),
    path('users-restaurants/<int:pk>/', RestaurantUserDetail.as_view(), name=RestaurantUserDetail.name),
    path('users-restaurants/<int:pk>/restaurants/', RestaurantByUserList.as_view(), name=RestaurantByUserList.name),
    path('users-restaurants/<int:pk>/restaurants/<int:id>/', RestaurantByUserDetail.as_view(), name=RestaurantByUserDetail.name),

    path('restaurants/', RestaurantList.as_view(), name=RestaurantList.name),
    path('restaurants/<int:pk>/', RestaurantDetail.as_view(), name=RestaurantDetail.name),
    path('restaurants/<int:pk>/dishes/', DishList.as_view(), name=DishList.name),
    path('restaurants/<int:pk>/dishes/<int:id>', DishDetail.as_view(), name=DishDetail.name),

    path('dishes/', DishAllList.as_view(), name=DishAllList.name),

    path('stats/', ApiStats.as_view(), name=ApiStats.name),
]