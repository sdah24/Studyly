from django.db import models
from django.conf import settings


class Notification(models.Model):

    TYPE_CHOICES = [
        ('application_update', 'Application Update'),
        ('deadline_reminder',  'Deadline Reminder'),
        ('scholarship_match',  'Scholarship Match'),
        ('document_required',  'Document Required'),
        ('general',            'General'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    type       = models.CharField(max_length=30, choices=TYPE_CHOICES, default='general')
    title      = models.CharField(max_length=255)
    message    = models.TextField()
    is_read    = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} — {self.title}"

    def icon_style(self):
        return {
            'application_update': {'bg': '#dcfce7', 'color': '#16a34a', 'icon': '✅'},
            'deadline_reminder':  {'bg': '#fee2e2', 'color': '#dc2626', 'icon': '📅'},
            'scholarship_match':  {'bg': '#f3e8ff', 'color': '#9333ea', 'icon': '🏆'},
            'document_required':  {'bg': '#ffedd5', 'color': '#ea580c', 'icon': '📄'},
            'general':            {'bg': '#dbeafe', 'color': '#2563eb', 'icon': 'ℹ️'},
        }.get(self.type, {'bg': '#f3f4f6', 'color': '#374151', 'icon': '🔔'})