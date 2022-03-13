from rest_framework import viewsets, status, permissions
from .serializers import CommentSerializer, PostSerializer
from .models import Category, Post
from rest_framework.response import Response


class PostView(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Post.objects.all().prefetch_related('categories')
        return queryset

    def perform_create(self, serializer):
        kwargs = {
            'author': self.request.user
        }
        serializer.save(**kwargs)

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            obj.views_count = obj.views_count + 1
            obj.save()
        return super().retrieve(request, *args, **kwargs)
