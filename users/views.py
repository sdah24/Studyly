from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from .models import User


def register_view(request):
    print("REGISTER VIEW HIT")
    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Password check
        if password != confirm_password:
            return render(
                request,
                "users/register.html",
                {"error": "Passwords do not match"}
            )

        # Save user
        User.objects.create(
            name=name,
            email=email,
            password=password
        )

        return redirect("login")

    return render(
        request,
        "users/register.html"
    )




def login_view(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)

            if user.password == password:
                return redirect("dashboard")

            else:
                return render(
                    request,
                    "users/login.html",
                    {"error": "Invalid password"}
                )

        except User.DoesNotExist:

            return render(
                request,
                "users/login.html",
                {"error": "Email not found"}
            )

    return render(
        request,
        "users/login.html"
    )