from django.contrib import admin

from .models import Recipe, Ingredient, Tag, IngredientAmount


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ["title", "dimension"]
    list_filter = ["title"]


@admin.register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = ["ingredient", "recipe", "amount"]
    list_filter = ["recipe"]


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ["title", "author"]
    list_filter = ["author", "title", "tags"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["title"]
