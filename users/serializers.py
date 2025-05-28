from rest_framework.fields import SerializerMethodField

from .models import CustomUser
from rest_framework.serializers import ModelSerializer, CharField
from django.contrib.auth.password_validation import validate_password


class UserSerializer(ModelSerializer):
    password = CharField(write_only=True, validators=[validate_password])

    def create(self, validated_data):
        validated_data['username'] = validated_data['email']
        user = CustomUser.objects.create_user(**validated_data)
        return user

    class Meta:
        model = CustomUser
        fields = ('email', 'password')
