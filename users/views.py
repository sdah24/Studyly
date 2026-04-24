from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .forms import RegisterForm, LoginForm, ProfileForm
from .models import User, Message
import os


# ─────────────────────────────────────────────────────────────────────────────
#  AUTH VIEWS
# ─────────────────────────────────────────────────────────────────────────────

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()          # form now sets user.role before saving
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
                old_path = profile.profile_picture.path
                profile.profile_picture.delete(save=False)
                profile.save(update_fields=['profile_picture'])
                if os.path.isfile(old_path):
                    os.remove(old_path)
                messages.success(request, 'Profile photo removed.')
            return redirect('users:profile')
        # ─────────────────────────────────────────────────────────────

        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
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


# ─────────────────────────────────────────────────────────────────────────────
#  MESSAGING VIEWS
# ─────────────────────────────────────────────────────────────────────────────

@login_required
def inbox_view(request):
    """Show all conversation threads for the logged-in user."""
    threads = Message.get_inbox_threads(request.user)
    all_users = User.objects.exclude(pk=request.user.pk).order_by('first_name', 'username')

    return render(request, 'users/messages.html', {
        'threads': threads,
        'all_users': all_users,
        'active_conversation': None,
    })


@login_required
def conversation_view(request, username):
    """Show + handle a single conversation between current user and <username>."""
    other_user = get_object_or_404(User, username=username)

    if other_user == request.user:
        return redirect('users:inbox')

    # Mark incoming messages as read
    Message.objects.filter(
        sender=other_user, recipient=request.user, is_read=False
    ).update(is_read=True)

    if request.method == 'POST':
        body = request.POST.get('body', '').strip()
        if body:
            Message.objects.create(
                sender=request.user,
                recipient=other_user,
                body=body,
            )
        return redirect('users:conversation', username=username)

    conversation_messages = Message.get_conversation(request.user, other_user)
    threads = Message.get_inbox_threads(request.user)
    all_users = User.objects.exclude(pk=request.user.pk).order_by('first_name', 'username')

    return render(request, 'users/messages.html', {
        'threads': threads,
        'all_users': all_users,
        'active_conversation': other_user,
        'conversation_messages': conversation_messages,
    })


@login_required
def new_conversation_view(request):
    """Start a conversation with someone the user hasn't messaged yet."""
    if request.method == 'POST':
        recipient_username = request.POST.get('recipient', '').strip()
        body = request.POST.get('body', '').strip()

        if recipient_username and body:
            recipient = get_object_or_404(User, username=recipient_username)
            if recipient != request.user:
                Message.objects.create(
                    sender=request.user,
                    recipient=recipient,
                    body=body,
                )
                return redirect('users:conversation', username=recipient_username)

    return redirect('users:inbox')