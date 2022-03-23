from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from django.urls import include, path
from .views import PostView, UploadImage, CommentView
from .utils import upvote, downvote

router = routers.DefaultRouter()
router.register(r'', PostView, basename='post')

urlpatterns = [
    path('', include(router.urls)),
]

utils_path = [
    path('utils/upvote/', upvote),
    path('utils/downvote/', downvote),
    path('utils/comment/', CommentView.as_view()),
    path('utils/upload/', UploadImage.as_view()),
]

urlpatterns += utils_path

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
