from django.db import models


class University(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    ranking = models.IntegerField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    # Extra fields for UI
    tuition_display = models.CharField(
        max_length=100, blank=True, null=True,
        help_text="e.g. $54,000/yr"
    )
    acceptance_rate = models.FloatField(
        blank=True, null=True,
        help_text="e.g. 4.5 for 4.5%"
    )
    rating = models.FloatField(blank=True, null=True, help_text="e.g. 4.9")
    total_students = models.CharField(max_length=50, blank=True, null=True)
    established_year = models.IntegerField(blank=True, null=True)
    min_gpa = models.FloatField(blank=True, null=True, help_text="Minimum GPA required")
    min_ielts = models.FloatField(blank=True, null=True, help_text="Minimum IELTS score")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['ranking']
        verbose_name_plural = 'Universities'

    def __str__(self):
        return self.name

    def ranking_display(self):
        return f"#{self.ranking}" if self.ranking else "N/A"


class Program(models.Model):
    LEVEL_CHOICES = [
        ('bachelor', "Bachelor's"),
        ('master', "Master's"),
        ('phd', 'PhD'),
        ('mba', 'MBA'),
    ]

    university = models.ForeignKey(
        University, on_delete=models.CASCADE, related_name='programs'
    )
    name = models.CharField(max_length=255)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='master')
    duration = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. 2 years")
    tuition_per_year = models.CharField(max_length=100, blank=True, null=True)
    requirements = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.university.name} — {self.name}"