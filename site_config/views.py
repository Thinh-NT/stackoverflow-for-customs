from rest_framework_simplejwt import views
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtain(TokenObtainPairSerializer):
    default_error_messages = {
        'no_active_account': {'detail': ['Username or Password does not matched.']}
    }


class CustomJWTCreate(views.TokenObtainPairView):
    serializer_class = CustomTokenObtain

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
