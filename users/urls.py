from django.urls import path
from . import views

urlpatterns = [

    path(
        "register/",
        views.register_view,
        name="register"
    ),

    path(
        "login/",
        views.login_view,
        name="login"
    ),

    path(
        "profile/create/",
        views.create_profile,
        name="create_profile"
    ),

]