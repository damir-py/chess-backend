import uuid

from rest_framework import serializers

from authentication.utils import generate_otp_code


class OTPSerializer(serializers.Serializer):
    otp_code = serializers.IntegerField(default=generate_otp_code)
    otp_key = serializers.UUIDField(default=uuid.uuid4)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=13)
    password = serializers.CharField(max_length=120)


