# Serializers

from rest_framework import serializers
from psbackend.models import User, Group, Photo, Membership

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'description', 'admin', 'created_at']
        read_only_fields = ['admin', 'created_at']

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'user', 'group', 'image_url', 'caption', 'uploaded_at']
        read_only_fields = ['user', 'group', 'uploaded_at']

class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ['user', 'group', 'joined_at']
        read_only_fields = ['joined_at']
