from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUser
from cars.models import Car, Comment


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["phone", "first_name", "last_name"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]


class CreateCarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ["make", "model", "year", "description"]

