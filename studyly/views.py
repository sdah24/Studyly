from django.shortcuts import render

def landing(request):
    # If user is already logged in, skip the landing page
    if request.user.is_authenticated:
        from django.shortcuts import redirect
        return redirect('dashboard:dashboard')
    return render(request, 'landing.html')