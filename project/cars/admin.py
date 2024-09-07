from django.contrib import admin
from .models import Car, Comment


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = (
        "make",
        "model",
        "year",
        "description",
        "created_at",
        "updated_at",
        "owner",
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("content", "created_at", "car", "author")
