"""
URL configuration for settings project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from main.views import RegisterView, CarList, Logout,Login,CarCreation, CarDetail, CarEdit, CarDelete




urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('api.urls'),name='api'),
    path('login/',Login.as_view(),name='login'),
    path('logout/',Logout.as_view(),name='logout'),
    path('reg/',RegisterView.as_view(),name='reg'),
    path('create/',CarCreation.as_view(),name='carcreate'),
    path('',CarList.as_view(),name='home'),
    path('car/<int:pk>/',CarDetail.as_view(),name='detail'),
    path('car/<int:pk>/edit/', CarEdit.as_view(),name='edit'),
    path('car/<int:pk>/delete/',CarDelete.as_view(),name='delete')
]
