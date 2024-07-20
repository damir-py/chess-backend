from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password

from .models import User, OTP
from .serializers import UserSerializer
from .utils import check_otp, send_otp, check_otp_expired, check_user


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
        return Response(data={'message': {obj_create.otp_key}, 'ok': True}, status=status.HTTP_201_CREATED)

    def verify(self, request):
        otp_code = request.data.get('otp_code')
        otp_key = request.data.get('otp_key')

        if not otp_code or not otp_key:
            return Response(
                data={'message': 'otp code ot kay not found!', 'ok': False},
                status=status.HTTP_400_BAD_REQUEST
            )

        obj_otp = OTP.objects.filter(otp_key=otp_key).first()
        if not obj_otp:
            return Response(
                data={'message': 'otp not found!', 'ok': False},
                status=status.HTTP_400_BAD_REQUEST
            )
        check_otp_expired(obj_otp)

        if obj_otp.attempts >= 1:
            return Response(
                data={'message': 'Please get new otp code and key!', 'ok': False},
                status=status.HTTP_400_BAD_REQUEST
            )

        if obj_otp.otp_code != otp_code:
            obj_otp.attempts += 1
            obj_otp.save(update_fields=['attempts'])
            return Response(
                data={'message': 'OTP code verification failed!', 'ok': False},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = obj_otp.user
        user.is_verified = True
        user.save(update_fields=['is_verified'])
        OTP.objects.filter(user_id=user.id).delete()
        return Response(
            data={'message': 'User successfully verified!', 'ok': True},
            status=status.HTTP_200_OK
        )

    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if username is None or password is None:
            return Response(
                data={'message': 'Please fill all the blanks!', 'ok': False},
                status=status.HTTP_400_BAD_REQUEST
            )

        obj_user = User.objects.filter(username=username).first()

        check_user(obj_user)

        if check_password(password, obj_user.password):
            refresh_token = str(RefreshToken.for_user(obj_user))
            access_token = str(refresh_token.access_token)
            return Response(
                data={'message': {'access_token': access_token, 'refresh_token': refresh_token}, 'ok': False},
                status=status.HTTP_200_OK
            )
        return Response(
            data={'message': 'Password is incorrect!', 'ok': False},
            status=status.HTTP_400_BAD_REQUEST
        )
