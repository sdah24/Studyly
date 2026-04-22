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

    # NEW FIELD
    category = models.CharField(
        max_length=50,
        choices=[
            ("merit", "Merit-Based"),
            ("need", "Need-Based"),
            ("sports", "Sports"),
            ("research", "Research"),
        ],
        default="merit"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return self.title