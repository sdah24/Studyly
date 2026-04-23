from django.db import models
from universities.models import University


class Scholarship(models.Model):

    CATEGORY_CHOICES = [
        ('merit', 'Merit-Based'),
        ('need', 'Need-Based'),
        ('sports', 'Sports'),
        ('research', 'Research'),
    ]

    FUNDING_TYPE_CHOICES = [
        ('full', 'Full Funding'),
        ('partial', 'Partial Funding'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    provider = models.CharField(max_length=255, blank=True, null=True)

    # University is optional — global scholarships aren't tied to one uni
    university = models.ForeignKey(
        University,
        on_delete=models.SET_NULL,
        related_name='scholarships',
        null=True,
        blank=True
    )

    # Amount
    amount = models.DecimalField(
        max_digits=12, decimal_places=2,
        null=True, blank=True
    )
    amount_display = models.CharField(
        max_length=150, blank=True, null=True,
        help_text="e.g. Full Tuition + Living Expenses"
    )

    funding_type = models.CharField(
        max_length=10,
        choices=FUNDING_TYPE_CHOICES,
        default='full'
    )

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='merit'
    )

    deadline = models.DateField()

    target_group = models.CharField(
        max_length=150, blank=True, null=True,
        help_text="e.g. Graduate Students"
    )

    recipients_per_year = models.CharField(
        max_length=50, blank=True, null=True,
        help_text="e.g. 4,000"
    )

    # Eligibility thresholds (used by eligibility module)
    min_gpa_required = models.FloatField(null=True, blank=True)
    min_ielts_required = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['deadline']

    def __str__(self):
        return self.title

    def is_full_funding(self):
        return self.funding_type == 'full'