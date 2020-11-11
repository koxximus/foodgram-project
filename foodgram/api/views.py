from django.db import IntegrityError
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from recipes.models import Ingredient, Recipe
from .models import Favorite, Follow, User, Purchase
from .viewsets import CreateDestroyViewSet
from .serializers import (IngredientSerializer,
                          FavoriteSerializer,
                          FollowSerializer,
                          PurchaseSerializer,
                          )


class ListIng(generics.ListAPIView):
    serializer_class = IngredientSerializer

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        title = self.request.query_params.get('query', None)
        queryset = queryset.filter(title__startswith=title)
        return queryset


class FavoriteViewSet(CreateDestroyViewSet):
    serializer_class = FavoriteSerializer
    lookup_field = "recipe__id"

    def get_queryset(self):
        queryset = Favorite.objects.filter(follower=self.request.user)
        return queryset

    def perform_create(self, serializer):
        try:
            follower = self.request.user
            recipe = generics.get_object_or_404(Recipe, id=self.request.data.get("id"))
            serializer.save(follower=follower, recipe=recipe)
        except IntegrityError:
            raise ValidationError({"detail": "This recipe are already in your favorite"})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.follower == self.request.user:
            self.perform_destroy(instance)
            return Response({"success": True})
        else:
            return Response({"success": False})


class FollowViewSet(CreateDestroyViewSet):
    serializer_class = FollowSerializer
    lookup_field = "following__id"

    def get_queryset(self):
        queryset = Follow.objects.filter(follower=self.request.user)
        return queryset

    def perform_create(self, serializer):
        try:
            follower = self.request.user
            following = generics.get_object_or_404(User, id=self.request.data.get("id"))
            serializer.save(follower=follower, following=following)
        except IntegrityError:
            raise ValidationError({"detail": "You are already following this author"})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.follower == self.request.user:
            self.perform_destroy(instance)
            return Response({"success": True})
        else:
            return Response({"success": False})


class PurchaceViewSet(CreateDestroyViewSet):
    serializer_class = PurchaseSerializer
    lookup_field = "recipe__id"

    def get_queryset(self):
        queryset = Purchase.objects.filter(customer=self.request.user)
        return queryset

    def perform_create(self, serializer):
        try:
            customer = self.request.user
            recipe = generics.get_object_or_404(Recipe, id=self.request.data.get("id"))
            serializer.save(customer=customer, recipe=recipe)
        except IntegrityError:
            raise ValidationError({"detail": "This recipe are already in your purchases"})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.customer == self.request.user:
            self.perform_destroy(instance)
            return Response({"success": True})
        else:
            return Response({"success": False})
