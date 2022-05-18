from django.utils.timezone import now
from rest_framework import serializers

from .models import Category, Comment, Image, Post


def td_format(td_object):
    seconds = int(td_object.total_seconds())
    periods = [
        ('year',        60*60*24*365),
        ('month',       60*60*24*30),
        ('day',         60*60*24),
        ('hour',        60*60),
        ('minute',      60),
        ('second',      1)
    ]

    strings = []
    for period_name, period_seconds in periods:
        if seconds > period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            has_s = 's' if period_value > 1 else ''
            strings.append("%s %s%s" % (period_value, period_name, has_s))

    return ", ".join(strings)


class UniModelSerializer(serializers.ModelSerializer):
    def get_field_names(self, declared_fields, info):
        expanded_fields = super(UniModelSerializer, self).get_field_names(
            declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields


class CategorySerializer(UniModelSerializer):
    class Meta:
        model = Category
        fields = ['title']


class ReplySerializer(UniModelSerializer):
    write_since = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Comment
        extra_fields = ['username']
        exclude = ['timestamp', 'user', 'post', 'parent']

    def get_write_since(self, obj):
        if td_format(now() - obj.timestamp) == '':
            return 'Just now'
        return td_format(now() - obj.timestamp) + ' ago'

    def get_is_owner(self, obj):
        request = self.context.get('request', None)
        if request:
            try:
                return request.user.email == obj.user.email
            except AttributeError:
                return False


class CommentSerializer(ReplySerializer):
    replies = serializers.SerializerMethodField()

    def get_replies(self, obj):
        serializer = ReplySerializer(obj.comment_set.all(), many=True)
        return serializer.data


class PostSerializer(UniModelSerializer):
    comments_count = serializers.IntegerField(required=False)
    upvotes_count = serializers.IntegerField(required=False)
    downvotes_count = serializers.IntegerField(required=False)

    categories = CategorySerializer(many=True)

    class Meta:
        model = Post
        exclude = ['author', 'people_involved']
        extra_fields = ['url', 'id', ]
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }

    def create(self, validated_data):
        categories = validated_data.pop('categories')
        post = Post.objects.create(**validated_data)
        for data in categories:
            title = ' '.join(data['title'].split())
            categories_query = Category.objects.filter(
                title__iexact=title)
            if categories_query.exists():
                post.categories.add(categories_query.first())
            else:
                post.categories.add(Category.objects.create(title=title))
        return post

    def update(self, instance, validated_data):
        categories = validated_data.pop('categories')
        instance.categories.clear()
        for data in categories:
            title = ' '.join(data['title'].split())
            categories_query = Category.objects.filter(
                title__iexact=title)
            if categories_query.exists():
                instance.categories.add(categories_query.first())
            else:
                instance.categories.add(Category.objects.create(title=title))

        return super().update(instance, validated_data)


class PostDetailSerializer(PostSerializer):
    class Meta:
        model = Post
        exclude = ['author', 'people_involved']
        extra_fields = ['url', 'id']
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('upload', 'timestamp')
