from .permissions import IsAdminOrOwner
from .serializers import (
    CarCreateSerializer,
    CarListSerializer,
    CommentCreateSerializer,
    CommentSerializer,
)
from users.models import CustomUser
from cars.models import Car, Comment
from rest_framework import serializers, status, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView


class CookieTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        access_token = response.data.get("access")
        refresh_token = response.data.get("refresh")
        response.set_cookie("access_token", access_token, httponly=True)
        response.set_cookie("refresh_token", refresh_token, httponly=True)
        return response


class CookieTokenRefreshView(TokenRefreshView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        access_token = response.data.get("access")
        refresh_token = response.data.get("refresh")
        if access_token:
            response.set_cookie(
                "access_token", access_token, httponly=True, secure=True
            )
        if refresh_token:
            response.set_cookie(
                "refresh_token", refresh_token, httponly=True, secure=True
            )
        return response


class LogoutView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        response = Response()
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        response.status_code = 204
        return response


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all().order_by("-created_at")
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = [
        "owner",
    ]

    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = [AllowAny]
        elif self.request.method == "POST":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminOrOwner]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return CarListSerializer
        return CarCreateSerializer  # для create,update,destroy и partial_update

    def perform_create(self, serializer):
        owner = self.request.user
        serializer.save(owner=owner)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by("-created_at")

    def get_queryset(self):
        car_id = self.kwargs["car_pk"]
        return self.queryset.filter(car_id=car_id)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return CommentSerializer
        return CommentCreateSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = [AllowAny]
        elif self.request.method == "POST":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)
