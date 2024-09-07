from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CarViewSet, CommentViewSet,CookieTokenObtainPairView, CookieTokenRefreshView, LogoutView

router = DefaultRouter()
router.register('cars', CarViewSet,basename='cars')

urlpatterns = [
    path('', include(router.urls)),
    path('cars/<int:car_pk>/comments/', CommentViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('cars/<int:car_pk>/comments/<int:pk>/', CommentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('auth/',include ('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/login/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
]