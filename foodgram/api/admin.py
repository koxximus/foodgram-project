from django.contrib import admin

from .models import Favorite, Follow, Purchase


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ["follower", "recipe"]


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ["following", "follower"]


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ["customer", "recipe"]
