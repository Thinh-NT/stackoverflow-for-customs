from django.http import JsonResponse
from notifications.models import Notification
from notifications.views import notify_user
from rest_framework import generics, status, views, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from .models import Comment, Post
from .serializers import (ImageSerializer, PostDetailSerializer,
                          PostSerializer, ReplySerializer)


def notify_to_group_people(to_, data):
    for x in to_:
        notify_user(x, data)


class PostView(viewsets.ModelViewSet):
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PostDetailSerializer
        return PostSerializer

    def get_queryset(self):
        queryset = Post.objects.all().prefetch_related(
            'categories')
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
    permission_classes = {
        "GET": [permissions.AllowAny],
        "POST": [permissions.IsAuthenticated]
    }

    def get_permissions(self):
        # Instances and returns the dict of permissions that the view requires.
        return {key: [permission() for permission in permissions] for key, permissions in self.permission_classes.items()}

    def check_permissions(self, request):
        # Gets the request method and the permissions dict, and checks the permissions defined in the key matching
        # the method.
        method = request.method
        for permission in self.get_permissions()[method]:
            if not permission.has_permission(request, self):
                self.permission_denied(
                    request, message=getattr(permission, 'message', None)
                )

    def post(self, request, *args, **kwargs):
        image_serializer = ImageSerializer(data=request.data)
        if image_serializer.is_valid():
            image = image_serializer.save()
        return JsonResponse(
            {
                "uploaded": True,
                "url": f'{image.upload.url}'
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
        return queryset.prefetch_related('user').order_by('-timestamp')

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({
                'Error': 'Login to comment'
            }, status=status.HTTP_401_UNAUTHORIZED)

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
                comment = Comment.objects.create(
                    user=request.user, post=post, content=content
                )
                people_involved = post.people_involved.exclude(
                    pk=request.user.pk)
                Notification.objects.bulk_create(
                    [
                        Notification(user=x, content='Someone comment at your post', reference=f'question/{post.slug}') for x in people_involved
                    ]
                )
                # Trigger message sent to group
                data = 'Someone comment at your post'
                notify_to_group_people(
                    people_involved, data
                )
                serializer = ReplySerializer(comment)
                return Response(serializer.data, status=202)

            except Post.DoesNotExist:
                return Response({
                    'Error': 'Post does not exists'
                }, status=status.HTTP_404_NOT_FOUND)

        if comment_id:
            try:
                comment = Comment.objects.get(id=comment_id)
                new_comment = Comment.objects.create(
                    user=request.user, parent=comment, content=content
                )
                serializer = ReplySerializer(new_comment)
                return Response(serializer.data, status=202)
            except Comment.DoesNotExist:
                return Response({
                    'Error': 'Comment does not exists'
                }, status=status.HTTP_404_NOT_FOUND)
