from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from users.models import User


@login_required
def community_list(request):
    query = request.GET.get('q', '').strip()
    role_filter = request.GET.get('role', 'all')

    users = User.objects.exclude(id=request.user.id).select_related('profile')

    if role_filter == 'student':
        users = users.filter(role='student')
    elif role_filter == 'consultant':
        users = users.filter(role='consultant')

    if query:
        users = users.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(username__icontains=query) |
            Q(profile__address__icontains=query)
        )

    students_count = User.objects.exclude(id=request.user.id).filter(role='student').count()
    consultants_count = User.objects.exclude(id=request.user.id).filter(role='consultant').count()

    context = {
        'users': users,
        'query': query,
        'role_filter': role_filter,
        'students_count': students_count,
        'consultants_count': consultants_count,
        'total_count': students_count + consultants_count,
        'active_nav': 'community',
    }
    return render(request, 'community/list.html', context)


@login_required
def community_profile(request, pk):
    profile_user = get_object_or_404(User, pk=pk)
    # Don't let users view their own profile here — redirect them
    context = {
        'profile_user': profile_user,
        'active_nav': 'community',
    }
    return render(request, 'community/profile.html', context)