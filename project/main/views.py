import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.views import View
from .forms import CustomUserCreationForm, CommentForm, CreateCarForm
from api.serializers import CarCreateSerializer, CommentCreateSerializer
from cars.models import Car
from api.views import CookieTokenObtainPairView


class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, "main/reg.html", {"form": form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            
            return redirect('login')
        return render(request, "main/reg.html", {"form": form})


class Login(View):
    def get(self, request):
        return render(request, "main/login.html")

    def post(self, request):
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        cookie_view = CookieTokenObtainPairView.as_view()
        response = cookie_view(request)

        user = authenticate(request, phone=phone, password=password)

        if response.status_code != 200 or not user:
            return HttpResponse("Auth credentials not provided")

        refresh = response.data.get("refresh")
        access = response.data.get("access")

        resp = HttpResponseRedirect(request.build_absolute_uri("/"))

        resp.set_cookie("refresh_token", refresh, httponly=True, secure=True)
        resp.set_cookie("access_token", access, httponly=True, secure=True)

        login(request, user=user)

        return resp


class Logout(View):
    def get(self, request):
        logout(request)
        rs = HttpResponseRedirect(request.build_absolute_uri("/"))
        rs.delete_cookie("refresh_token")
        rs.delete_cookie("access_token")
        return rs


class CarList(View):
    def get(self, request):
        response = requests.get(request.build_absolute_uri("/api/cars/"))
        cars = response.json() if response.status_code == 200 else []
        return render(request, "main/home.html", {"cars": cars})


class CarCreation(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self, request):
        form = CreateCarForm
        return render(request, "main/create_car.html", {"form": form})

    def post(self, request):
        form = CreateCarForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data["owner"] = request.user.id
            serializer = CarCreateSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return redirect("home")
        return render(request, "main/create_car.html", {"form": form})


class CarDetail(View):
    def get(self, request, pk):
        response = requests.get(request.build_absolute_uri(f"/api/cars/{pk}/"))
        car = response.json() if response.status_code == 200 else []
        comment_resp = requests.get(
            request.build_absolute_uri(f"/api/cars/{pk}/comments/")
        )  # также идея была реализовать данный endpoint иначе, в viewset комментариев по аналогии с
        comments = (
            comment_resp.json() if comment_resp.status_code == 200 else []
        )  # CarViewSet можно добавить filter backends и filterset_fields
        form = CommentForm()
        return render(
            request,
            "main/detail.html",
            {"car": car, "form": form, "comments": comments},
        )
    def post(self, request, pk):
        if not request.user.is_authenticated:
            return HttpResponse('Not logged in',status=401)
        data = request.POST.copy()
        data["author"] = request.user.id
        data["car"] = pk
        serializer = CommentCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return redirect(request.path)
        else:
            return redirect(request.path)


class CarEdit(LoginRequiredMixin,View):
    login_url = 'login'
    def get_car(self, pk):
        response = requests.get(self.request.build_absolute_uri(f"/api/cars/{pk}/"))
        if response.status_code == 200:
            return response.json()
        return None

    def check_permissions(self, request, car):
        return request.user.is_authenticated and (
            request.user.id == car["owner"] or request.user.is_staff
        )

    def get(self, request, pk):
        car = self.get_car(pk)
        if car and self.check_permissions(request, car):
            form = CreateCarForm(initial=car)
            return render(request, "main/edit_car.html", {"form": form})

        return HttpResponse("Permission denied", status=403)

    def post(self, request, pk):
        car_data = self.get_car(pk)
        if car_data and self.check_permissions(request, car_data):
            data = request.POST.copy()
            data["owner"] = car_data["owner"]["id"]

            serializer = CarCreateSerializer(data=data)

            if serializer.is_valid():
                car_instance = Car.objects.get(pk=pk)
                serializer.update(car_instance, serializer.validated_data)
                return redirect(request.build_absolute_uri(f"/car/{pk}/"))

            return HttpResponse(serializer.error_messages, status=400)

        return HttpResponse("Permission denied", status=403)


class CarDelete(View):  # вьюшкu CarEdit и CarDelete отличаются так сильно потому, что в CarDelete пользователь не вводит никаких данных.
    def get(self, request, pk):
        if not request.user.is_authenticated:
            return HttpResponse("Permission denied", status=403)
        try:
            car_instance = Car.objects.get(pk=pk)
        except Car.DoesNotExist:
            return render(request, "404.html", status=404)
        if request.user.id != car_instance.owner and not request.user.is_staff:
            return HttpResponse("Permission denied", status=403)

        return render(request, "main/delete.html")

    def post(self, request, pk):
        if not request.user.is_authenticated:
            return HttpResponse("Permission denied", status=403)
        try:
            car_instance = Car.objects.get(pk=pk)
        except Car.DoesNotExist:
            return render(request, "404.html", status=404)
        if request.user.id != car_instance.owner and not request.user.is_staff:
            return HttpResponse("Permission denied", status=403)
        car_instance.delete()
        return redirect("home")
