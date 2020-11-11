from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("favorites", views.FavoriteViewSet, basename="favorites")
router.register("subscriptions", views.FollowViewSet, basename="subscriptions")
router.register("purchases", views.PurchaceViewSet, basename="purchases")


urlpatterns = [
    path("ingredients/", views.ListIng.as_view(), name="get_ingredients"),
    path("", include(router.urls)),
]
