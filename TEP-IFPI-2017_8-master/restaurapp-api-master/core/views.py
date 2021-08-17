from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework import permissions
from .serializers import *
from .permissions import *
from rest_framework.filters import OrderingFilter, SearchFilter
# Create your views here.

class ApiRoot(generics.GenericAPIView):
    """
    Return the main urls.
    """
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({'profiles': reverse(UserList.name, request=request),
            'profiles-restaurants': reverse(RestaurantUserList.name, request=request),
            'restaurants': reverse(RestaurantList.name, request=request),
            'dishes': reverse(DishAllList.name, request=request),
            'stats': reverse(ApiStats.name, request=request),
            })

class UserList(generics.ListCreateAPIView):
    """
    get:
    Return all user profiles.
    """
    queryset = PersonProfile.objects.all()
    name = 'user-list'
    http_method_names = ('get','post')
    filter_backends = (OrderingFilter, SearchFilter)
    ordering_fields = ('username', 'name')
    search_fields = ('username', 'name')
    permission_classes = (IsAdmin,)

    def get_serializer_class(self):
        if self.request.method=='GET':
            return UserSerializer
        elif self.request.method=='POST':
            return PostUserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
    Return a single person profile.

    put:
    Update an instance of person profile.

    delete:
    Delete an instance of person profile.
    """
    serializer_class = UserSerializer
    name = 'user-detail'
    http_method_names = ['get','put','delete']
    permission_classes = (IsAdmin, IsHimHerItSelf)

    def get_queryset(self):
        return PersonProfile.objects.get(pk=self.kwargs['pk'])

class RestaurantUserList(generics.ListCreateAPIView):
    """
    get:
    Return all restaurant profiles.

    post:
    Create a new restaurant profile.
    """
    queryset = RestaurantProfile.objects.all()
    name = 'user-restaurants-list'
    http_method_names = ['get', 'post']
    permission_classes = (IsAdmin,)

    def get_serializer_class(self):
        if self.request.method=='GET':
            return UserRestaurantSerializer
        elif self.request.method=='POST':
            return PostUserRestaurantSerializer


class RestaurantUserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
    Return a single restaurant profile.

    put:
    Update an instance of restaurant profile.

    delete:
    Delete an instance of restaurant profile.
    """
    serializer_class = UserRestaurantSerializer
    name = 'user-restaurants-detail'
    http_method_names = ('get', 'put','delete')
    permission_classes = (IsAdmin,IsHimHerItSelf)

    def get_queryset(self):
        return User.objects.get(id=self.kwargs['pk'])


class RestaurantByUserList(generics.ListCreateAPIView):
    """
    get:
    Return all the restaurants of a user.

    post:
    Create a new restaurant.
    """
    serializer_class = RestaurantSerializer
    name = 'restaurant-by-user-list'
    http_method_names = ('get','post')
    permission_classes = (permissions.IsAuthenticated, IsRestaurante, IsOwner)

    def get_queryset(self):
        return RestaurantProfile.objects.get(id=self.kwargs['pk']).restaurants

class RestaurantByUserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
    Return a restaurant related to a user.

    put:
    Update an instance of a restaurant.

    delete:
    Delete an instance of a restaurant.
    """
    serializer_class = RestaurantSerializer
    name = 'restaurant-by-user-detail'
    http_method_names = ('get','put','delete')
    permission_classes = (IsRestaurante,)

    def get_queryset(self):
        profile = RestaurantProfile.objects.get(id=self.kwargs['pk'])
        return Restaurant.objects.get(id=self.kwargs['id'], profile=profile)

class RestaurantList(generics.ListCreateAPIView):
    """
    get:
    Return all the restaurants.

    post:
    Create a new restaurant.
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    name = 'restaurant-list'
    http_method_names = ['get','post']
    filter_backends = (OrderingFilter, SearchFilter)
    ordering_fields = ('phone', 'name')
    search_fields = ('phone', 'name')
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsRestaurante,)

    def get_serializer_class(self):
        if self.request.method=='GET':
            return RestaurantSerializer
        elif self.request.method=='POST':
            return PostRestaurantSerializer

class RestaurantDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
    Return a single restaurant.

    put:
    Update an instance of restaurant.

    delete:
    Delete an instance of restaurant.
    """
    serializer_class = RestaurantSerializer
    name = 'restaurant-detail'
    http_method_names = ['get','put','delete']

    def get_queryset(self):
        return Restaurant.objects.get(id=self.kwargs['pk'])

class DishList(generics.ListCreateAPIView):
    """
    get:
    Return all dishes related to a restaurante

    post:
    Create an instance of order.
    """
    serializer_class = DishSerializer
    name = 'dish-list'
    http_method_names = ['get','post']

    def get_queryset(self):
        return RestaurantProfile.objects.get(id=self.kwargs['pk']).dishes

class DishAllList(generics.ListCreateAPIView):
    """
    get:
    Return all dishes.

    post:
    Create a new dish.
    """
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    name = 'dish-public-list'
    http_method_names = ['get']
    filter_backends = (OrderingFilter, SearchFilter)
    ordering_fields = ('name', 'description', 'price')
    search_fields = ('name',)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsRestaurante,)

class DishDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
    Return a single dish.

    put:
    Update an instance of a dish.

    delete:
    Delete an instance of a dish
    """
    serializer_class = DishSerializerDetailed
    name = 'dish-detail'
    http_method_names = ['get','put','delete']

    def get_queryset(self):
        restaurant = RestaurantProfile.objects.get(id=self.kwargs['pk'])
        return Dish.objects.get(id=self.kwargs['id'], restaurant=restaurant)

class OrderList(generics.ListCreateAPIView):
    """
    get:
    Return all orders related to a user.

    post:
    Create a new order.
    """
    serializer_class = OrderSerializer
    name = 'order-list'
    http_method_names = ['get','post']
    permission_classes = (permissions.IsAuthenticated, IsPerson, IsAdmin)

    filter_backends = (OrderingFilter, SearchFilter)
    ordering_fields = ('created', 'status',)
    search_fields = ('created',)

    def get_queryset(self):
        user = PersonProfile.objects.get(id=self.kwargs['pk'])
        return user.orders

class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
    Return a single order.

    put:
    Update an instance of order.

    delete:
    Delete an instance of order.
    """
    serializer_class = OrderSerializer
    name = 'order-detail'
    http_method_names = ['get','put','delete']
    permission_classes = (permissions.IsAuthenticated, IsPerson, IsAdmin)

    def get_queryset(self):
        user = PersonProfile.objects.get(id=self.kwargs['pk'])
        return Order.objects.get(id=self.kwargs['id'], customer=user)

class ApiStats(APIView):
    """
    Return the number of restaurants and dishes.
    """
    parser_classes = (MultiPartParser,)
    name = 'api-stats'

    def get(self, request, *args, **kwargs):
        return Response({'restaurants':Restaurant.objects.count(), 'dishes': Dish.objects.count()}, status=status.HTTP_200_OK)