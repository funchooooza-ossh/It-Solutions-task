from djoser.serializers import (
    UserCreateSerializer as BaseUserCreateSerializer,
    UserSerializer as BaseUserSerializer,
    TokenCreateSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import serializers
from cars.models import Car, Comment
from users.models import CustomUser


class UserCreateSerializer(BaseUserCreateSerializer):

    class Meta(BaseUserCreateSerializer.Meta):
        model = CustomUser
        fields = ["phone", "password", "first_name", "last_name"]

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserSerializer(BaseUserSerializer):

    class Meta:
        model = CustomUser
        fields = ["id", "first_name", "last_name", "is_staff"]


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):

    post = serializers.StringRelatedField(read_only=True, many=False)
    author = UserSerializer(read_only=True, many=False)
    author_first_name = serializers.CharField(
        source="author.first_name", read_only=True
    )
    author_last_name = serializers.CharField(source="author.last_name", read_only=True)
    formatted_create = serializers.SerializerMethodField()

    def get_formatted_create(self, obj):
        return obj.created_at.strftime("%d-%m-%Y %H:%M")

    class Meta:
        model = Comment
        fields = "__all__"


class CarCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = "__all__"

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def delete(self, instance):
        try:
            instance.delete()
            return None
        except Exception as e:
            raise e


class CarListSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField(read_only=True)
    owner = UserSerializer(read_only=True)
    owner_first_name = serializers.CharField(source="owner.first_name", read_only=True)
    owner_last_name = serializers.CharField(source="owner.last_name", read_only=True)
    formatted_create = serializers.SerializerMethodField()
    formatted_update = serializers.SerializerMethodField()

    def get_comments_count(self, obj):
        return obj.comment_set.count()

    def get_formatted_create(self, obj):
        return obj.created_at.strftime("%d-%m-%Y %H:%M")

    def get_formatted_update(self, obj):
        return obj.updated_at.strftime("%d-%m-%Y %H:%M")

    class Meta:
        model = Car
        fields = "__all__"
