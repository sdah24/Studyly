from django.db import models

# Create your models here.
from django.db import models
from universities.models import University


class Scholarship(models.Model):

    title = models.CharField(
        max_length=255
    )

    description = models.TextField()

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    deadline = models.DateField()

    university = models.ForeignKey(
        University,
        on_delete=models.CASCADE,
        related_name="scholarships"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return self.title