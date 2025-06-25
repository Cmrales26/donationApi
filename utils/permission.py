# apps/campaign/permissions.py

from rest_framework.permissions import BasePermission, SAFE_METHODS


class havePermission(BasePermission):
    """
    Permite acceso de escritura solo a usuarios en el grupo con ID 1.
    Permite lectura a cualquier usuario autenticado.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated

        return (
            request.user
            and request.user.is_authenticated
            and request.user.groups.filter(id=1).exists()
        )


class IsAdminOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user
            and request.user.is_authenticated
            and (request.user.groups.filter(id=1).exists() or obj.user == request.user)
        )
