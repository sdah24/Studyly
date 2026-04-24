from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('', views.community_list, name='list'),
    path('<int:pk>/', views.community_profile, name='profile'),
]