
from django.urls import path
from . import views

app_name = "universities"
urlpatterns = [
     path("universities/",
          views.universities_view,
          name = "universities"),
    path(

        "",

        views.university_search,

        name="search"

    ),
path(

    "detail/<int:pk>/",

    views.university_detail,

    name="detail"

),
]



