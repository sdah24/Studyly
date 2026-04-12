
from django.urls import path
from . import views

urlpatterns = [
     path("universities/",
          views.universities_view,
          name = "universities"),
]