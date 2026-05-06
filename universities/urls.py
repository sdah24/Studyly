from django.urls import path
from . import views

app_name = 'universities'

urlpatterns = [
    path('',                          views.university_list,     name='list'),
    path('<int:pk>/',                 views.university_detail,   name='detail'),
    path('<int:pk>/programs/',        views.university_programs, name='programs'),
]