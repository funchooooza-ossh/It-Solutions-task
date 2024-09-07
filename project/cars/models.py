from django.db import models
from users.models import CustomUser


class Car(models.Model):
    make = models.CharField(
        max_length=30,  # magic number anyway
        null=False,
        blank=False,
        verbose_name="Марка",
    )
    model = models.CharField(
        max_length=30, null=False, blank=False, verbose_name="Модель"
    )
    year = models.PositiveIntegerField(
        null=False, blank=False, verbose_name="Год выпуска"
    )
    description = models.TextField(
        max_length=200,  # I think this field should be edited depending on the format of such a site,
        null=False,  # that is, do we want to see giant descriptions or do we want users to briefly summarize the essence
        blank=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,  # same problem. If we want to delete all posts after deleting user we should use models.CASCADE, otherwise PROTECT(bad idea imho),RESTRICT(better)
        # or SET_NULL(not bad), SET_DEFAULT(in this way whe should set default value),DO_NOTHING(in this way we should manually fix problems after user delete)
        null=False,
        blank=False,
    )

    def __str__(self):
        return f"{self.make} {self.model} {self.year}"


class Comment(models.Model):
    content = models.TextField(max_length=100, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, blank=False, null=False)
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, blank=False, null=False
    )
