from django.db import models

# Create your models here.

from django.db import models


class User(models.Model):

    user_id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)

    password = models.CharField(max_length=255)

    role = models.CharField(
        max_length=20,
        default="student"
    )

    GPA = models.FloatField(null=True, blank=True)

    budget = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    preferred_countries = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name