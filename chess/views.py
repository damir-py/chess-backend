from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .models import User, OTP
from .serializers import UserSerializer
from .utils import check_otp, send_otp


class AuthenticationAPIView(ViewSet):
    def register(self, request):
        data = request.data
        user = User.objects.filter(username=data.get['username']).first()
        if user.is_verified:
            return Response(
                data={'message': 'User already exists.', 'ok': False},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = UserSerializer(user, data=data, partial=True) if user else UserSerializer(data=data)

        if not serializer.is_valid():
            return Response(
                data={'message': serializer.errors, 'ok': False},
                status=status.HTTP_400_BAD_REQUEST
            )
        validated_data = serializer.save()
        obj_create = OTP.objects.create(user_id=validated_data.id)
        obj_all = OTP.objects.filter(user_id=validated_data.id)

        check_otp(obj_all)

        obj_create.save()
        send_otp(obj_create)
