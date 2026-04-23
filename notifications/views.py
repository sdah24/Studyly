from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render
from .models import Notification


@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user)

    # Filter tab
    tab = request.GET.get('tab', 'all')
    if tab == 'unread':
        notifications = notifications.filter(is_read=False)
    elif tab == 'applications':
        notifications = notifications.filter(type='application_update')
    elif tab == 'scholarships':
        notifications = notifications.filter(type='scholarship_match')

    unread_count = Notification.objects.filter(
        user=request.user, is_read=False
    ).count()

    return render(request, 'notifications/notifications.html', {
        'notifications': notifications,
        'unread_count':  unread_count,
        'active_tab':    tab,
    })


@login_required
def mark_read(request, pk):
    notif = get_object_or_404(Notification, pk=pk, user=request.user)
    notif.is_read = True
    notif.save()
    return redirect('notifications:list')


@login_required
def mark_all_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    messages.success(request, 'All notifications marked as read.')
    return redirect('notifications:list')


@login_required
def delete_notification(request, pk):
    notif = get_object_or_404(Notification, pk=pk, user=request.user)
    if request.method == 'POST':
        notif.delete()
    return redirect('notifications:list')