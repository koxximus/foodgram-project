from django.contrib.auth import get_user_model
from django.db import models
from rest_framework.exceptions import ValidationError

from recipes.models import Recipe

User = get_user_model()


class Favorite(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="favorites"
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="favorites"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["follower", "recipe"], name="unique_favorites"
            )
        ]
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"


class Follow(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower"
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author"
    )

    class Meta:
        unique_together = ["follower", "following"]
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def clean(self):
        if self.follower == self.following:
            raise ValidationError("You can not follow yourself")


class Purchase(models.Model):
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="purchases"
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="purchases"
    )

    class Meta:
        unique_together = ["customer", "recipe"]
        verbose_name = "Список покупок"
        verbose_name_plural = "Списки покупок"
