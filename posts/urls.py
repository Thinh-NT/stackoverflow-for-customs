from rest_framework import routers
from django.urls import include, path
from .views import PostView
from .utils import upvote, downvote

router = routers.DefaultRouter()
router.register(r'', PostView, basename='post')

urlpatterns = [
    path('', include(router.urls)),
]

utils_path = [
    path('utils/upvote/', upvote),
    path('utils/downvote/', downvote),
]

urlpatterns += utils_path
