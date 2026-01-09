from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwner(BasePermission):
    """Доступ только к своим привычкам."""

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsPublicReadOnly(BasePermission):
    """Разрешает только чтение публичных привычек."""

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return obj.is_public
        return False
