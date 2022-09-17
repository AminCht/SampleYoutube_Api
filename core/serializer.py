from djoser.serializers import UserCreateSerializer as BaseUserCreateSer, UserSerializer as BaseUserSer
from rest_framework import serializers


class UserCreateSerializer(BaseUserCreateSer):
    class Meta(BaseUserCreateSer.Meta):
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']


class UserSerializer(BaseUserSer):
    class Meta(BaseUserSer.Meta):
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'email']


class ActivationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()


class RedeemCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=255)
