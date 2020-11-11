from rest_framework import serializers

from recipes.models import Ingredient
from .models import Favorite, Follow, Purchase


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["title", "dimension"]


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = "__all__"
        read_only_fields = ["follower", "recipe"]


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = "__all__"
        read_only_fields = ["follower", "following"]


class PurchaseSerializer(serializers.ModelSerializer):
    recipe = serializers.ReadOnlyField(source="recipe.id")

    class Meta:
        model = Purchase
        fields = "__all__"
        read_only_fields = ["customer"]
