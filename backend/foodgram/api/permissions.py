from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Model
from rest_framework.permissions import DjangoModelPermissions  # noqa F401
from rest_framework.permissions import IsAuthenticated  # noqa F401
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.routers import APIRootView


# class BasePermission(BasePermission):
#     """Базовый класс разрешений с проверкой - забанен ли пользователь."""

#     def has_permission(self, request, view):
#         return bool(
#             request.method in SAFE_METHODS
#             or request.user.is_authenticated
#             and request.user.is_active
#         )


class AuthorStaffOrReadOnly(BasePermission):
    """
    Разрешение на изменение только для служебного персонала и автора.
    Остальным только чтение объекта.
    """

    def has_object_permission(
        self, request: WSGIRequest, view: APIRootView, obj: Model
    ) -> bool:
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_active
            and (request.user == obj.author or request.user.is_staff)
        )


class AdminOrReadOnly(BasePermission):
    """
    Разрешение на создание и изменение только для админов.
    Остальным только чтение объекта.
    """
    
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_active
            and request.user.is_staff
        )


    def has_object_permission(self, request, view, obj):
        print(f'USER IS STAFF: {request.user.is_staff}')
        return (
            request.method in SAFE_METHODS
            or (request.user.is_authenticated
            and request.user.is_active
            and request.user.is_staff)
        )


class OwnerUserOrReadOnly(BasePermission):
    """
    Разрешение на создание и изменение только для админа и пользователя.
    Остальным только чтение объекта.
    """

    def has_object_permission(
        self, request: WSGIRequest, view: APIRootView, obj: Model
    ) -> bool:
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_active
            and request.user == obj.author
            or request.user.is_staff
        )
