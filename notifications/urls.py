from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from django.urls import include, path
from .views import NotificationView

router = routers.DefaultRouter()
router.register(r'', NotificationView, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
