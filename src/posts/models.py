from django.db import models
from django.contrib.auth import get_user_model
from autoslug import AutoSlugField


User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    overview = models.TextField()
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    views_count = models.IntegerField(default=0)

    categories = models.ManyToManyField(Category, related_name='posts')

    slug = AutoSlugField(populate_from='title',
                         unique_with=['author__username', 'timestamp__day'])

    def __str__(self):
        return self.title

    def comments_count(self):
        return self.comments.count()

    def upvotes_count(self):
        return self.upvote_set.count()

    def downvotes_count(self):
        return self.downvote_set.count()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey(
        Post,
        related_name='comments',
        on_delete=models.CASCADE
    )
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True)


class DownVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, blank=True, null=True)
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, blank=True, null=True)


class UpVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, blank=True, null=True)
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, blank=True, null=True)
