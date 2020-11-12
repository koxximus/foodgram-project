from rest_framework.permissions import IsAuthenticatedOrReadOnly


class IsFollowerOrReadOnly(IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        return bool(obj.follower == request.user or request.user.is_superuser)


class IsCustomerOrReadOnly(IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        return bool(obj.customer == request.user or request.user.is_superuser)
