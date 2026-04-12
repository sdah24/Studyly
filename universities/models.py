from django.db import models

# Create your models here.


class University(models.Model):

    name = models.CharField(max_length=200)

    country = models.CharField(max_length=100)

    tuition_range = models.CharField(max_length=100)

    intake = models.CharField(max_length=50)

    description = models.TextField()

    def __str__(self):
        return self.name