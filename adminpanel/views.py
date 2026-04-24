from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from users.models import User
from universities.models import University, Program
from scholarships.models import Scholarship
from applications.models import Application


# ── Role guard decorator ───────────────────────────────────────────────────────
def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:login')
        if request.user.role != 'admin':
            return redirect('dashboard:dashboard')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


# ── Dashboard ──────────────────────────────────────────────────────────────────
@admin_required
def dashboard(request):
    total_students      = User.objects.filter(role='student').count()
    total_universities  = University.objects.count()
    total_applications  = Application.objects.count()
    total_scholarships  = Scholarship.objects.count()

    recent_applications = Application.objects.select_related(
        'user', 'university', 'program'
    ).order_by('-applied_date')[:8]

    context = {
        'total_students':     total_students,
        'total_universities': total_universities,
        'total_applications': total_applications,
        'total_scholarships': total_scholarships,
        'recent_applications': recent_applications,
        'active_sidebar': 'dashboard',
    }
    return render(request, 'adminpanel/dashboard.html', context)


# ── Students ───────────────────────────────────────────────────────────────────
@admin_required
def students(request):
    q = request.GET.get('q', '').strip()
    student_list = User.objects.filter(role='student').select_related('profile').order_by('-date_joined')
    if q:
        student_list = student_list.filter(username__icontains=q) | \
                       student_list.filter(email__icontains=q) | \
                       student_list.filter(first_name__icontains=q) | \
                       student_list.filter(last_name__icontains=q)

    context = {
        'students':       student_list,
        'q':              q,
        'active_sidebar': 'students',
    }
    return render(request, 'adminpanel/students.html', context)


# ── Universities ───────────────────────────────────────────────────────────────
@admin_required
def universities(request):
    uni_list = University.objects.all().order_by('ranking')
    context = {
        'universities':   uni_list,
        'active_sidebar': 'universities',
    }
    return render(request, 'adminpanel/universities.html', context)


@admin_required
def university_create(request):
    if request.method == 'POST':
        University.objects.create(
            name=request.POST.get('name'),
            country=request.POST.get('country'),
            city=request.POST.get('city'),
            ranking=request.POST.get('ranking') or None,
            rating=request.POST.get('rating') or None,
            tuition_display=request.POST.get('tuition_display'),
            acceptance_rate=request.POST.get('acceptance_rate') or None,
            min_gpa=request.POST.get('min_gpa') or None,
            min_ielts=request.POST.get('min_ielts') or None,
            website=request.POST.get('website'),
            description=request.POST.get('description'),
        )
        messages.success(request, 'University added successfully.')
        return redirect('adminpanel:universities')
    return render(request, 'adminpanel/university_form.html', {'active_sidebar': 'universities', 'action': 'Add'})


@admin_required
def university_edit(request, pk):
    uni = get_object_or_404(University, pk=pk)
    if request.method == 'POST':
        uni.name           = request.POST.get('name')
        uni.country        = request.POST.get('country')
        uni.city           = request.POST.get('city')
        uni.ranking        = request.POST.get('ranking') or None
        uni.rating         = request.POST.get('rating') or None
        uni.tuition_display = request.POST.get('tuition_display')
        uni.acceptance_rate = request.POST.get('acceptance_rate') or None
        uni.min_gpa        = request.POST.get('min_gpa') or None
        uni.min_ielts      = request.POST.get('min_ielts') or None
        uni.website        = request.POST.get('website')
        uni.description    = request.POST.get('description')
        uni.save()
        messages.success(request, 'University updated successfully.')
        return redirect('adminpanel:universities')
    return render(request, 'adminpanel/university_form.html', {
        'uni': uni, 'active_sidebar': 'universities', 'action': 'Edit'
    })


@admin_required
def university_delete(request, pk):
    uni = get_object_or_404(University, pk=pk)
    if request.method == 'POST':
        uni.delete()
        messages.success(request, 'University deleted.')
        return redirect('adminpanel:universities')
    return render(request, 'adminpanel/confirm_delete.html', {
        'object_name': uni.name, 'active_sidebar': 'universities',
        'cancel_url': 'adminpanel:universities',
    })


# ── Scholarships ───────────────────────────────────────────────────────────────
@admin_required
def scholarships(request):
    schol_list = Scholarship.objects.all().order_by('deadline')
    context = {
        'scholarships':   schol_list,
        'active_sidebar': 'scholarships',
    }
    return render(request, 'adminpanel/scholarships.html', context)


@admin_required
def scholarship_create(request):
    universities = University.objects.all().order_by('name')
    if request.method == 'POST':
        from datetime import date
        Scholarship.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            provider=request.POST.get('provider'),
            university_id=request.POST.get('university') or None,
            amount=request.POST.get('amount') or None,
            amount_display=request.POST.get('amount_display'),
            funding_type=request.POST.get('funding_type', 'full'),
            category=request.POST.get('category', 'merit'),
            deadline=request.POST.get('deadline'),
            target_group=request.POST.get('target_group'),
            recipients_per_year=request.POST.get('recipients_per_year'),
            min_gpa_required=request.POST.get('min_gpa_required') or None,
            min_ielts_required=request.POST.get('min_ielts_required') or None,
        )
        messages.success(request, 'Scholarship added successfully.')
        return redirect('adminpanel:scholarships')
    return render(request, 'adminpanel/scholarship_form.html', {
        'universities': universities, 'active_sidebar': 'scholarships', 'action': 'Add'
    })


@admin_required
def scholarship_edit(request, pk):
    schol = get_object_or_404(Scholarship, pk=pk)
    universities = University.objects.all().order_by('name')
    if request.method == 'POST':
        schol.title              = request.POST.get('title')
        schol.description        = request.POST.get('description')
        schol.provider           = request.POST.get('provider')
        schol.university_id      = request.POST.get('university') or None
        schol.amount             = request.POST.get('amount') or None
        schol.amount_display     = request.POST.get('amount_display')
        schol.funding_type       = request.POST.get('funding_type', 'full')
        schol.category           = request.POST.get('category', 'merit')
        schol.deadline           = request.POST.get('deadline')
        schol.target_group       = request.POST.get('target_group')
        schol.recipients_per_year = request.POST.get('recipients_per_year')
        schol.min_gpa_required   = request.POST.get('min_gpa_required') or None
        schol.min_ielts_required = request.POST.get('min_ielts_required') or None
        schol.save()
        messages.success(request, 'Scholarship updated successfully.')
        return redirect('adminpanel:scholarships')
    return render(request, 'adminpanel/scholarship_form.html', {
        'schol': schol, 'universities': universities,
        'active_sidebar': 'scholarships', 'action': 'Edit'
    })


@admin_required
def scholarship_delete(request, pk):
    schol = get_object_or_404(Scholarship, pk=pk)
    if request.method == 'POST':
        schol.delete()
        messages.success(request, 'Scholarship deleted.')
        return redirect('adminpanel:scholarships')
    return render(request, 'adminpanel/confirm_delete.html', {
        'object_name': schol.title, 'active_sidebar': 'scholarships',
        'cancel_url': 'adminpanel:scholarships',
    })