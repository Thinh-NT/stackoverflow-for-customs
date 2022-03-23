from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets, status, permissions
from .serializers import CommentSerializer, PostSerializer, ImageSerializer, ReplySerializer, PostDetailSerializer
from .models import Category, Comment, Post, Image
from rest_framework.response import Response
from rest_framework import views
from rest_framework import generics


class PostView(viewsets.ModelViewSet):
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PostDetailSerializer
        return PostSerializer

    def get_queryset(self):
        queryset = Post.objects.all().prefetch_related('categories')
        return queryset.order_by('-timestamp')

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


class UploadImage(views.APIView):
    def post(self, request, *args, **kwargs):
        image_serializer = ImageSerializer(data=request.data)
        if image_serializer.is_valid():
            image = image_serializer.save()
        return JsonResponse(
            {
                "uploaded": True,
                "url": f'http://localhost:8000/media/{image.upload.name}'
            }
        )


class CommentView(generics.ListAPIView):
    serializer_class = ReplySerializer

    # def get_serializer_class(self):
    #     comment_id = self.request.query_params.get('comment_id')
    #     if comment_id:
    #         return ReplySerializer
    #     return CommentSerializer

    def get_queryset(self):
        post_id = self.request.query_params.get('post_id')
        comment_id = self.request.query_params.get('comment_id')
        if not (post_id or comment_id):
            queryset = Comment.objects.none()
        if post_id:
            try:
                post = Post.objects.get(id=post_id)
                queryset = post.comments.all()
            except Post.DoesNotExist:
                queryset = Comment.objects.none()

        if comment_id:
            try:
                comment = Comment.objects.get(id=comment_id)
                queryset = comment.comment_set.all()
            except Comment.DoesNotExist:
                queryset = Comment.objects.none()
        return queryset

    def post(self, request, *args, **kwargs):
        post_id = request.data.get('post_id')
        comment_id = request.data.get('comment_id')
        content = request.data.get('content')

        if not (post_id or comment_id):
            return Response({
                'Error': 'Provide post or comment'
            }, status=status.HTTP_406_NOT_ACCEPTABLE)

        if not content:
            return Response({
                'Error': 'Enter content to submit comment'
            }, status=status.HTTP_406_NOT_ACCEPTABLE)

        if post_id:
            try:
                post = Post.objects.get(id=post_id)
                Comment.objects.create(
                    user=request.user, post=post, content=content
                )
            except Post.DoesNotExist:
                return Response({
                    'Error': 'Post does not exists'
                }, status=status.HTTP_404_NOT_FOUND)
            return HttpResponse(post.downvote_set.count(), status=202)

        if comment_id:
            try:
                comment = Comment.objects.get(id=comment_id)
                Comment.objects.create(
                    user=request.user, parent=comment, content=content
                )
            except Comment.DoesNotExist:
                return Response({
                    'Error': 'Comment does not exists'
                }, status=status.HTTP_404_NOT_FOUND)

            return HttpResponse(status=202)
