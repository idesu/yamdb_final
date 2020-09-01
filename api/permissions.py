from rest_framework.permissions import IsAdminUser, SAFE_METHODS, BasePermission


class IsAdminUserOrReadOnly(IsAdminUser):

    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return request.method in SAFE_METHODS or is_admin


class IsOwnerOrAdminOrModerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        # всегда разрешены GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # всё разрешено модераторам и админам
        if request.user.role in ('admin', 'moderator', ):
            return True

        # всё разрешено автору отзыва
        return obj.author == request.user
