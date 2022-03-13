from turtle import title
from rest_framework import serializers

from .models import Post, Comment, Category


class UniModelSerializer(serializers.HyperlinkedModelSerializer):
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


class CommentSerializer(UniModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class PostSerializer(UniModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    comments_count = serializers.IntegerField(required=False)
    upvotes_count = serializers.IntegerField(required=False)
    downvotes_count = serializers.IntegerField(required=False)

    categories = CategorySerializer(many=True)

    class Meta:
        model = Post
        exclude = ['author']
        extra_fields = ['url', 'id']
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
