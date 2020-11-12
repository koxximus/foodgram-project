from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import Ingredient, Recipe, User

from .models import Favorite, Follow, Purchase


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["title", "dimension"]


class FavoriteSerializer(serializers.ModelSerializer):
    id = serializers.SlugRelatedField(
        slug_field="id", queryset=Recipe.objects.all(), source="recipe"
    )
    follower = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Favorite
        fields = ["id", "follower"]
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=["follower", "id"],
                message="This recipe are already in your favorite",
            )
        ]

    def validate_id(self, value):
        follower = self.context["request"].user
        if follower == value.author:
            raise ValidationError("You can not to add your recipe in favorite")
        return value


class FollowSerializer(serializers.ModelSerializer):
    id = serializers.SlugRelatedField(
        slug_field="id", queryset=User.objects.all(), source="following"
    )
    follower = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Follow
        fields = ["id", "follower"]
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=["follower", "id"],
                message="You are already following this author",
            )
        ]


class PurchaseSerializer(serializers.ModelSerializer):
    id = serializers.SlugRelatedField(
        slug_field="id", queryset=Recipe.objects.all(), source="recipe"
    )
    customer = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Purchase
        fields = ["id", "customer"]
        validators = [
            UniqueTogetherValidator(
                queryset=Purchase.objects.all(),
                fields=["id", "customer"],
                message="This recipe are already in your purchases",
            )
        ]

    def validate_id(self, value):
        customer = self.context["request"].user
        if customer == value.author:
            raise ValidationError(
                "You can not to add your recipe in purchases"
            )
        return value
