from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("favorites", views.FavoriteViewSet, basename="favorites")
router.register("subscriptions", views.FollowViewSet, basename="subscriptions")
router.register("purchases", views.PurchaceViewSet, basename="purchases")


urlpatterns = [
    path("v1/ingredients/", views.ListIng.as_view(), name="get_ingredients"),
    path("v1/", include(router.urls)),
]
