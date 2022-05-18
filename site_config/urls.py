from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.views.static import serve
from .views import CustomJWTCreate
from notifications.views import home  # Importing basic home view
from notifications.views import notification_test_page


# DRF YASG
schema_view = get_schema_view(
    openapi.Info(
        title="STACKOVERHERE",
        default_version="v1",
        description="REST implementation of UNI system.",
        contact=openapi.Contact(email="thanhthinhkrb@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # YASG
    re_path(
        r"^api/docs/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),


    # noti
    path("", home, name="home"),
    path("notifications-test/", notification_test_page, name="notifications-test"),

    # Djoser
    path('auth/jwt/create/', CustomJWTCreate.as_view()),
    path('', include('accounts.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    # Users
    path("api/accounts/", include("accounts.urls")),

    # Apps
    path("api/posts/", include("posts.urls")),
    path("api/notifications/", include("notifications.urls")),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT
        }),
    ]
