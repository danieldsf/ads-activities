from django.contrib.auth.models import UserManager
from django.db.models import Manager
from .enums import *

class CaseInsensitiveUserManager(UserManager):
    
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})

class PersonProfileManager(Manager):
    def get_queryset(self):
        return super(PersonProfileManager, self).get_queryset().filter(user_type=UserType.CLIENTE)

class RestaurantProfileManager(Manager):
    def get_queryset(self):
        return super(RestaurantProfileManager, self).get_queryset().filter(user_type=UserType.RESTAURANTE)
