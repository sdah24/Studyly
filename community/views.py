from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from users.models import User
from .models import ConsultantRequest


@login_required
def community_list(request):
    query       = request.GET.get('q', '').strip()
    role_filter = request.GET.get('role', 'all')

    users = User.objects.exclude(id=request.user.id).select_related('profile')

    if role_filter == 'student':
        users = users.filter(role='student')
    elif role_filter == 'consultant':
        users = users.filter(role='consultant')

    if query:
        users = users.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)  |
            Q(username__icontains=query)   |
            Q(profile__address__icontains=query)
        )

    # Build a set of consultant IDs the current student has already requested
    existing_requests = {}
    if request.user.role == 'student':
        for cr in ConsultantRequest.objects.filter(student=request.user):
            existing_requests[cr.consultant_id] = cr.status

    # Pending requests waiting for this consultant to act
    pending_incoming = []
    if request.user.role == 'consultant':
        pending_incoming = ConsultantRequest.objects.filter(
            consultant=request.user, status='pending'
        ).select_related('student', 'student__profile')

    students_count   = User.objects.exclude(id=request.user.id).filter(role='student').count()
    consultants_count = User.objects.exclude(id=request.user.id).filter(role='consultant').count()

    return render(request, 'community/list.html', {
        'users':             users,
        'query':             query,
        'role_filter':       role_filter,
        'students_count':    students_count,
        'consultants_count': consultants_count,
        'total_count':       students_count + consultants_count,
        'existing_requests': existing_requests,
        'pending_incoming':  pending_incoming,
        'active_nav':        'community',
    })


@login_required
def community_profile(request, pk):
    profile_user = get_object_or_404(User, pk=pk)

    cr = None
    if request.user.role == 'student' and profile_user.role == 'consultant':
        cr = ConsultantRequest.objects.filter(
            student=request.user, consultant=profile_user
        ).first()

    # Applications this student has shared with this consultant
    shared_applications = []
    if request.user.role == 'student' and profile_user.role == 'consultant':
        from applications.models import Application
        shared_applications = Application.objects.filter(
            user=request.user,
            shared_with_consultant=True
        ).select_related('university', 'program')

    return render(request, 'community/profile.html', {
        'profile_user':        profile_user,
        'consultant_request':  cr,
        'shared_applications': shared_applications,
        'active_nav':          'community',
    })


@login_required
def request_consultant(request, pk):
    """Student sends a guidance request to a consultant."""
    if request.user.role != 'student':
        return redirect('community:list')

    consultant = get_object_or_404(User, pk=pk, role='consultant')
    note       = request.POST.get('note', '').strip()

    obj, created = ConsultantRequest.objects.get_or_create(
        student=request.user,
        consultant=consultant,
        defaults={'note': note}
    )
    if created:
        messages.success(request, f'Request sent to {consultant.get_full_name() or consultant.username}.')
        # Notify consultant
        from notifications.models import Notification
        Notification.objects.create(
            user=consultant,
            type='general',
            title=f'{request.user.get_full_name() or request.user.username} requested your guidance',
            message=note[:200] if note else 'A student has requested your guidance.',
        )
    else:
        messages.info(request, 'You have already sent a request to this consultant.')

    return redirect('community:profile', pk=pk)


@login_required
def respond_request(request, pk):
    """Consultant accepts or rejects a request."""
    if request.user.role != 'consultant':
        return redirect('community:list')

    cr     = get_object_or_404(ConsultantRequest, pk=pk, consultant=request.user)
    action = request.POST.get('action')  # 'accept' or 'reject'

    if action == 'accept':
        cr.status       = 'accepted'
        cr.responded_at = timezone.now()
        cr.save()
        # Set assigned_consultant on student's profile
        profile = cr.student.profile
        profile.assigned_consultant = request.user
        profile.save(update_fields=['assigned_consultant'])
        messages.success(request, f'You are now connected with {cr.student.get_full_name() or cr.student.username}.')
        from notifications.models import Notification
        Notification.objects.create(
            user=cr.student,
            type='general',
            title='Consultant accepted your request',
            message=f'{request.user.get_full_name() or request.user.username} has accepted your guidance request.',
        )
    elif action == 'reject':
        cr.status       = 'rejected'
        cr.responded_at = timezone.now()
        cr.save()
        messages.info(request, 'Request rejected.')

    return redirect('community:list')


@login_required
def share_application(request, app_pk):
    """Student toggles sharing an application with their consultant."""
    from applications.models import Application
    app = get_object_or_404(Application, pk=app_pk, user=request.user)
    app.shared_with_consultant = not app.shared_with_consultant
    app.save(update_fields=['shared_with_consultant'])
    state = 'shared' if app.shared_with_consultant else 'unshared'
    messages.success(request, f'Application {state} with your consultant.')
    return redirect('applications:detail', pk=app_pk)


@login_required
def consultant_student_view(request, student_pk):
    """Consultant views a connected student's shared applications and files."""
    if request.user.role != 'consultant':
        return redirect('community:list')

    student = get_object_or_404(User, pk=student_pk, role='student')

    # Verify connection
    cr = ConsultantRequest.objects.filter(
        student=student, consultant=request.user, status='accepted'
    ).first()
    if not cr:
        messages.error(request, 'You are not connected with this student.')
        return redirect('community:list')

    from applications.models import Application
    shared_apps = Application.objects.filter(
        user=student, shared_with_consultant=True
    ).select_related('university', 'program')

    return render(request, 'community/student_view.html', {
        'student':     student,
        'shared_apps': shared_apps,
        'active_nav':  'community',
    })