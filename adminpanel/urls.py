from django.urls import path
from . import views

app_name = 'adminpanel'

urlpatterns = [
    path('',                                  views.dashboard,           name='dashboard'),
    path('students/',                         views.students,            name='students'),
    path('students/<int:pk>/promote/',        views.promote_to_admin,    name='promote_to_admin'),
    path('universities/',                     views.universities,        name='universities'),
    path('universities/add/',                 views.university_create,   name='university_create'),
    path('universities/<int:pk>/edit/',       views.university_edit,     name='university_edit'),
    path('universities/<int:pk>/delete/',     views.university_delete,   name='university_delete'),
    path('scholarships/',                     views.scholarships,        name='scholarships'),
    path('scholarships/add/',                 views.scholarship_create,  name='scholarship_create'),
    path('scholarships/<int:pk>/edit/',       views.scholarship_edit,    name='scholarship_edit'),
    path('scholarships/<int:pk>/delete/',     views.scholarship_delete,  name='scholarship_delete'),
]