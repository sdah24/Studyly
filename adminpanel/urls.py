from django.urls import path
from . import views

urlpatterns = [

    path(
        "adminpanel/",
        views.admin_dashboard_view,
        name="adminpanel"
    ),

]