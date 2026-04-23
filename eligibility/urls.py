from django.urls import path
from . import views

app_name = 'eligibility'

urlpatterns = [
    path('check/', views.check, name='check'),
]