from django.conf import settings
from django.conf.urls import handler404, handler500  # noqa
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import include, path

handler404 = "foodgram.views.page_not_found"  # noqa
handler500 = "foodgram.views.server_error"  # noqa

urlpatterns = [
    path("admin/", admin.site.urls),
    path("about/", include("django.contrib.flatpages.urls")),
    path("auth/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path("api/", include("api.urls")),
]

urlpatterns += [
    path(
        "about-author/",
        views.flatpage,
        {"url": "/about-author/"},
        name="author",
    ),
    path("about-spec/", views.flatpage, {"url": "/about-spec/"}, name="spec"),
    path("", include("recipes.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
