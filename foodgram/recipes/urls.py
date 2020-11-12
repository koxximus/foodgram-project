from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.new_recipe, name="new_recipe"),
    path("<str:username>/", views.author_page, name="author_page"),
    path("<str:username>/follow/", views.follow_page, name="my_follow"),
    path(
        "<str:username>/<int:recipe_id>", views.recipe_page, name="recipe_page"
    ),
    path(
        "<str:username>/<int:recipe_id>/edit/",
        views.recipe_edit,
        name="recipe_edit",
    ),
    path(
        "<str:username>/<int:recipe_id>/del/",
        views.recipe_del,
        name="recipe_del",
    ),
    path("<str:username>/favorites/", views.my_favorites, name="my_favorites"),
    path("<str:username>/shoplist/", views.shoplist, name="shoplist"),
    path(
        "<str:username>/shoplist/download/",
        views.download_shoplist,
        name="download_shoplist",
    ),
]
