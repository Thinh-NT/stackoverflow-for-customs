from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

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

    # Djoser
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    # Users
    path("api/accounts/", include("accounts.urls")),

    # Apps
    path("api/posts/", include("posts.urls")),
]
