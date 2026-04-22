from django.urls import path
from . import views

from django.urls import path
app_name = 'dashboard'
urlpatterns = [path('', views.dashboard, name='dashboard'),]