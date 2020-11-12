from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    title = models.CharField(max_length=10)
    color = models.CharField(max_length=20)
    value = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    title = models.CharField(max_length=200)
    dimension = models.CharField(max_length=20)

    class Meta:
        unique_together = ["title", "dimension"]
        verbose_name = "Игредиент"
        verbose_name_plural = "Игредиенты"

    def __str__(self):
        return self.title


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recipes"
    )
    title = models.CharField("названием", max_length=200, unique=True)
    image = models.ImageField(upload_to="recipes/")
    description = models.TextField(null=False, blank=False)
    ingredients = models.ManyToManyField(
        Ingredient, related_name="recipes", through="IngredientAmount"
    )
    tags = models.ManyToManyField(Tag, related_name="recipes")
    time = models.PositiveSmallIntegerField()
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.title


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name="ingredient_amounts"
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="ingredient_amounts"
    )
    amount = models.IntegerField()

    class Meta:
        verbose_name = "Состав"
        verbose_name_plural = "Состав"

    def __str__(self):
        return f"{self.ingredient.title}({self.ingredient.dimension}) - {self.amount}"
