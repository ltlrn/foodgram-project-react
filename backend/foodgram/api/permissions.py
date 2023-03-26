from rest_framework.permissions import SAFE_METHODS, BasePermission


class AuthorStaffOrReadOnly(BasePermission):
    """
    Автор и персонал - изменение,
    Прочие - чтение.
    """

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_active
            and (
                request.user == obj.author
                or request.user.is_staff
            )
        )


class AdminOrReadOnly(BasePermission):
    """
    Админ - создание и изменение,
    Прочие - чтение.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_active
            and request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS
            or (
                request.user.is_authenticated
                and request.user.is_active
                and request.user.is_staff
            )
        )
    