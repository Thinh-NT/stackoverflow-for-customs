from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView,)
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile
from .serializers import UserProfileSerializer
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.decorators import action


class UserProfileListCreateView(ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class UserProfileDetailView(RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]


class UsersViewSet(DjoserUserViewSet):

    @action(['get', 'put', 'delete'], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        elif request.method == "PUT":
            return self.update(request, *args, **kwargs)
        elif request.method == "DELETE":
            return self.destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        data = request.data
        # data.pop('profile_picture', False)

        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        profile_picture = request.FILES.get('profile_picture')
        if profile_picture:
            profile = instance.profile
            profile_serialize = UserProfileSerializer(
                instance.profile, data={'profile_picture': profile_picture})
            profile_serialize.is_valid(raise_exception=True)
            self.perform_update(profile_serialize)

        profile = data.pop('profile', None)
        if profile:
            profile.pop('profile_picture', False)
            profile_serialize = UserProfileSerializer(
                instance.profile, data=profile)
            profile_serialize.is_valid(raise_exception=True)
            self.perform_update(profile_serialize)

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return super().update(request, *args, **kwargs)
