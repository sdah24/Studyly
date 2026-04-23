from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
#from applications.models import Application
#from notifications.models import Notification
from scholarships.models import Scholarship


@login_required
def dashboard(request):
    user = request.user

    # Application stats
    applications = Application.objects.filter(user=user)
    total_apps     = applications.count()
    accepted_apps  = applications.filter(status='accepted').count()
    pending_apps   = applications.filter(
        status__in=['submitted', 'under_review', 'incomplete']
    ).count()

    # Recent applications (latest 3)
    recent_apps = applications.select_related(
        'university', 'program'
    ).order_by('-applied_date')[:3]

    # Upcoming deadlines (next 3 by deadline)
    upcoming = applications.filter(
        deadline__gte=timezone.now().date()
    ).order_by('deadline')[:3]

    # Available scholarships count
    scholarships_count = Scholarship.objects.filter(
        deadline__gte=timezone.now().date()
    ).count()

    # Unread notifications
    unread_notifications = Notification.objects.filter(
        user=user, is_read=False
    ).count()

    return render(request, 'dashboard/dashboard.html', {
        'total_apps': total_apps,
        'accepted_apps': accepted_apps,
        'pending_apps': pending_apps,
        'recent_apps': recent_apps,
        'upcoming': upcoming,
        'scholarships_count': scholarships_count,
        'unread_notifications': unread_notifications,
    })


@login_required
def profile_view(request):
    # Redirect to users profile page
    return redirect('users:profile')