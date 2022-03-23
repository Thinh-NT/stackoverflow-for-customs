from .models import Comment, Post
from django.db.models.signals import pre_save, pre_delete, post_save


def add_comments_count(comment):
    if comment.parent:
        comment.parent.replies_count += 1
        comment.parent.save()
        add_comments_count(comment.parent)
    if comment.post:
        comment.post.comments_count += 1
        comment.post.save()


def subtract_comments_count(comment):
    if comment.parent:
        comment.parent.replies_count -= 1
        comment.parent.save()
        subtract_comments_count(comment.parent)
    if comment.post:
        comment.post.comments_count -= 1
        comment.post.save()


# SIGNALS
def pre_save_comment(sender, instance, **kwargs):
    # When new comment posted
    if not instance.id:
        add_comments_count(instance)
    if instance.post:
        instance.post.people_involved.add(instance.user)
    if instance.parent:
        instance.parent.post.people_involved.add(instance.user)


def pre_delete_comment(sender, instance, **kwargs):
    subtract_comments_count(instance)


def post_post_save(sender, instance, **kwargs):
    instance.people_involved.add(instance.author)


post_save.connect(post_post_save, Post)
pre_save.connect(pre_save_comment, Comment)
pre_delete.connect(pre_delete_comment, Comment)
