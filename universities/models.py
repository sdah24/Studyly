from django.db import models


class University(models.Model):

    name = models.CharField(
        max_length=255
    )

    country = models.CharField(
        max_length=100
    )

    city = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    ranking = models.IntegerField(
        blank=True,
        null=True
    )

    website = models.URLField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = ["name"]

    def __str__(self):

        return self.name