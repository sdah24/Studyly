from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Application
from .forms import ApplicationForm
from universities.models import University, Program


@login_required
def application_list(request):
    applications = Application.objects.filter(
        user=request.user
    ).select_related('university', 'program')

    # Status filter tab
    status_filter = request.GET.get('status', '')
    if status_filter:
        applications = applications.filter(status=status_filter)

    # Counts for mini stat cards
    all_apps      = Application.objects.filter(user=request.user)
    total         = all_apps.count()
    accepted      = all_apps.filter(status='accepted').count()
    under_review  = all_apps.filter(status='under_review').count()
    incomplete    = all_apps.filter(status='incomplete').count()
    rejected      = all_apps.filter(status='rejected').count()

    return render(request, 'applications/applications.html', {
        'applications':  applications,
        'status_filter': status_filter,
        'total':         total,
        'accepted':      accepted,
        'under_review':  under_review,
        'incomplete':    incomplete,
        'rejected':      rejected,
    })


@login_required
def application_create(request):
    # Pre-select university if passed via ?university=<pk>
    initial = {}
    uni_pk = request.GET.get('university')
    if uni_pk:
        try:
            initial['university'] = University.objects.get(pk=uni_pk)
        except University.DoesNotExist:
            pass

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.user = request.user
            app.save()
            messages.success(request, f'Application to {app.university.name} created!')
            return redirect('applications:detail', pk=app.pk)
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = ApplicationForm(initial=initial)

    return render(request, 'applications/application_form.html', {
        'form': form,
        'title': 'New Application',
    })


@login_required
def application_detail(request, pk):
    app = get_object_or_404(Application, pk=pk, user=request.user)
    return render(request, 'applications/application_detail.html', {'app': app})


@login_required
def application_update(request, pk):
    app = get_object_or_404(Application, pk=pk, user=request.user)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, instance=app)
        if form.is_valid():
            form.save()
            messages.success(request, 'Application updated!')
            return redirect('applications:detail', pk=app.pk)
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = ApplicationForm(instance=app)

    return render(request, 'applications/application_form.html', {
        'form': form,
        'app': app,
        'title': f'Edit — {app.university.name}',
    })


@login_required
def application_delete(request, pk):
    app = get_object_or_404(Application, pk=pk, user=request.user)
    if request.method == 'POST':
        name = app.university.name
        app.delete()
        messages.success(request, f'Application to {name} deleted.')
        return redirect('applications:list')
    return render(request, 'applications/application_confirm_delete.html', {'app': app})