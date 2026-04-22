from django.urls import path
from . import views

urlpatterns = [

    path(
        "eligibility/",
        views.eligibility_view,
        name="eligibility"
    ),

]