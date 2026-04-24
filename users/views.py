from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileForm
import os


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to Studyly, {user.first_name}!')
            return redirect('dashboard:dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            next_url = request.GET.get('next', 'dashboard:dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('users:login')


@login_required
def profile_view(request):
    profile = request.user.profile

    if request.method == 'POST':

        # ── Handle photo removal ──────────────────────────────────────
        if request.POST.get('remove_picture') == '1':
            if profile.profile_picture:
                # Delete the actual file from disk
                old_path = profile.profile_picture.path
                profile.profile_picture.delete(save=False)   # clears the field
                profile.save(update_fields=['profile_picture'])
                if os.path.isfile(old_path):
                    os.remove(old_path)
                messages.success(request, 'Profile photo removed.')
            return redirect('users:profile')
        # ─────────────────────────────────────────────────────────────

        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # If user uploaded a new photo, delete the old file first
            if 'profile_picture' in request.FILES and profile.profile_picture:
                old_path = profile.profile_picture.path
                if os.path.isfile(old_path):
                    os.remove(old_path)

            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('users:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'users/profile.html', {
        'form': form,
        'profile': profile,
    })