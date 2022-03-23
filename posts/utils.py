from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from django.http import HttpResponse
from .models import Post, Comment, UpVote, DownVote
from rest_framework.response import Response
from rest_framework import status


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def upvote(request):
    post_id = request.data.get('post_id')
    comment_id = request.data.get('comment_id')

    if not (post_id or comment_id):
        return Response({
            'Error': 'Provide post or comment'
        }, status=status.HTTP_406_NOT_ACCEPTABLE)

    if post_id:
        try:
            post = Post.objects.get(id=post_id)
            obj, upvoted = UpVote.objects.get_or_create(
                user=request.user, post=post)
            if not upvoted:
                obj.delete()
        except Post.DoesNotExist:
            return Response({
                'Error': 'Post does not exists'
            }, status=status.HTTP_404_NOT_FOUND)
        return HttpResponse(post.upvote_set.count(), status=202)

    if comment_id:
        try:
            comment = Comment.objects.get(id=post_id)
            obj, upvoted = UpVote.objects.get_or_create(
                user=request.user, comment=comment)
            if not upvoted:
                obj.delete()
        except Comment.DoesNotExist:
            return Response({
                'Error': 'Post does not exists'
            }, status=status.HTTP_404_NOT_FOUND)

        return HttpResponse(comment.upvote_set.count(), status=202)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def downvote(request):
    post_id = request.data.get('post_id')
    comment_id = request.data.get('comment_id')

    if not (post_id or comment_id):
        return Response({
            'Error': 'Provide post or comment'
        }, status=status.HTTP_406_NOT_ACCEPTABLE)

    if post_id:
        try:
            post = Post.objects.get(id=post_id)
            obj, downvotes = DownVote.objects.get_or_create(
                user=request.user, post=post)
            if not downvotes:
                obj.delete()
        except Post.DoesNotExist:
            return Response({
                'Error': 'Post does not exists'
            }, status=status.HTTP_404_NOT_FOUND)
        return HttpResponse(post.downvote_set.count(), status=202)

    if comment_id:
        try:
            comment = Comment.objects.get(id=post_id)
            obj, downvotes = DownVote.objects.get_or_create(
                user=request.user, comment=comment)
            if not downvotes:
                obj.delete()
        except Comment.DoesNotExist:
            return Response({
                'Error': 'Post does not exists'
            }, status=status.HTTP_404_NOT_FOUND)

        return HttpResponse(comment.downvote_set.count(), status=202)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def comment(request):
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
