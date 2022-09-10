from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import UserModel

class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        post=UserModel(**validated_data)
        post.save()
        return validated_data

    class Meta:
        model = UserModel
        fields = ['username', 'password', 'is_staff', 'is_artist','date_joined']

        extra_kwargs = {
            'password': {'write_only': True}
        }
