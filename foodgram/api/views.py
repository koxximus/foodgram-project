from rest_framework import filters, generics

from recipes.models import Ingredient, Recipe

from .models import Favorite, Follow, Purchase
from .permissions import IsCustomerOrReadOnly
from .serializers import (
    FavoriteSerializer,
    FollowSerializer,
    IngredientSerializer,
    PurchaseSerializer,
)
from .viewsets import CreateDestroyViewSet


class ListIng(generics.ListAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["^title"]


class FavoriteViewSet(CreateDestroyViewSet):
    serializer_class = FavoriteSerializer
    lookup_field = "recipe__id"

    def get_queryset(self):
        queryset = Favorite.objects.filter(follower=self.request.user)
        return queryset


class FollowViewSet(CreateDestroyViewSet):
    serializer_class = FollowSerializer
    lookup_field = "following__id"

    def get_queryset(self):
        queryset = Follow.objects.filter(follower=self.request.user)
        return queryset


class PurchaceViewSet(CreateDestroyViewSet):
    serializer_class = PurchaseSerializer
    lookup_field = "recipe__id"
    permission_classes = [IsCustomerOrReadOnly]

    def get_queryset(self):
        queryset = Purchase.objects.filter(customer=self.request.user)
        return queryset

    def perform_create(self, serializer):
        customer = self.request.user
        serializer.save(customer=customer)
