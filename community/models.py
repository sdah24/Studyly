from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings


class ConsultantRequest(models.Model):
    STATUS_CHOICES = [
        ('pending',  'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    student    = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='consultant_requests_sent'
    )
    consultant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='consultant_requests_received'
    )
    status       = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    note         = models.TextField(blank=True, null=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        # One pending/accepted request per student–consultant pair
        unique_together = ['student', 'consultant']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.username} → {self.consultant.username} ({self.status})"