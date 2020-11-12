from rest_framework import mixins, viewsets
from rest_framework.response import Response

from .permissions import IsFollowerOrReadOnly


class CreateDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [IsFollowerOrReadOnly]

    def perform_create(self, serializer):
        follower = self.request.user
        serializer.save(follower=follower)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.delete():
            return Response({"success": True})
        else:
            return Response({"success": False})
