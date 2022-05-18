from attr import field
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import UserProfile
from djoser.serializers import UserSerializer

User = get_user_model()

BACKEND_URL = 'http://192.168.1.96:8080'


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("id", "email", "username",
                  "first_name", "last_name", "password")


class ProfilePictureField(serializers.ImageField):
    def to_representation(self, value):
        return BACKEND_URL + str(value.url)


class UserProfileSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField(read_only=True)
    # profile_picture = serializers.URLField(source='profile_picture.url')
    date_joined = serializers.DateTimeField(
        format="%Y-%m-%d", read_only=True)
    updated_on = serializers.DateTimeField(
        format="%Y-%m-%d", read_only=True)
    reputation_points = serializers.IntegerField(read_only=True)
    profile_picture = ProfilePictureField()

    # def get_profile_picture_url(self, obj):
    #     obj.refresh_from_db()
    #     return BACKEND_URL + str(obj.profile_picture.url)

    class Meta:
        model = UserProfile
        exclude = ('user', )


class UniUserSerializer(UserSerializer):
    profile = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField(read_only=True)
    username = serializers.CharField(read_only=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    def get_profile(self, obj):
        return UserProfileSerializer(obj.profile).data

    def get_full_name(self, obj):
        return obj.first_name + ' ' + obj.last_name

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields
        fields += ('profile', 'full_name')
