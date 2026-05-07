from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('',                                        views.community_list,          name='list'),
    path('<int:pk>/',                               views.community_profile,       name='profile'),
    path('<int:pk>/request/',                       views.request_consultant,      name='request_consultant'),
    path('requests/<int:pk>/respond/',              views.respond_request,         name='respond_request'),
    path('applications/<int:app_pk>/share/',        views.share_application,       name='share_application'),
    path('students/<int:student_pk>/',              views.consultant_student_view, name='student_view'),
]