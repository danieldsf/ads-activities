from rest_framework import permissions
from .enums import UserType
from .models import User

class IsHimHerItSelf(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		return obj.pk == request.user

class IsOwner(permissions.IsAuthenticated):
	def has_object_permission(self, request, view, obj):
		return obj.owner == request.user

class IsAdmin(permissions.BasePermission):

	def has_permission(self, request, view):
		return permissions.IsAuthenticated.has_permission(self, request, view) and request.user.is_superuser

class IsPerson(permissions.IsAuthenticated):

	def has_permission(self, request, view, obj):
		return permissions.IsAuthenticated.has_permission(self, request, view) and request.user.user_type == UserType.CLIENTE and obj.owner == request.user

class IsRestaurante(permissions.IsAuthenticated):

	def has_object_permission(self, request, view, obj):
		return permissions.IsAuthenticated.has_permission(self, request, view) and request.user.user_type == UserType.RESTAURANTE and obj.owner == request.user