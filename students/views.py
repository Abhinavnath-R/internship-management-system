from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from accounts.decorators import student_required
from companies.models import Internship
from .models import StudentProfile, Application, Notification
from .forms import StudentProfileForm, ApplicationForm

@login_required
@student_required
def dashboard(request):
    profile = request.user.student_profile
    total_applications = profile.applications.count()
    pending_count = profile.applications.filter(status='pending').count()
    shortlisted_count = profile.applications.filter(status='shortlisted').count()
    accepted_count = profile.applications.filter(status='accepted').count()
    rejected_count = profile.applications.filter(status='rejected').count()
    recent_applications = profile.applications.select_related('internship__company').order_by('-applied_at')[:5]
    
    context = {
        'profile': profile,
        'total_applications': total_applications,
        'pending_count': pending_count,
        'shortlisted_count': shortlisted_count,
        'accepted_count': accepted_count,
        'rejected_count': rejected_count,
        'recent_applications': recent_applications,
    }
    return render(request, 'students/dashboard.html', context)

@login_required
@student_required
def profile(request):
    return render(request, 'students/profile.html', {'profile': request.user.student_profile})

@login_required
@student_required
def edit_profile(request):
    profile = request.user.student_profile
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('students:profile')
    else:
        form = StudentProfileForm(instance=profile)
        
    return render(request, 'students/edit_profile.html', {'form': form, 'profile': profile})

@login_required
@student_required
def browse_internships(request):
    internships = Internship.objects.filter(is_approved=True, is_active=True, application_deadline__gte=date.today(), company__is_verified=True).order_by('-created_at')
    
    q = request.GET.get('q', '')
    type_filter = request.GET.get('type', '')
    location = request.GET.get('location', '')
    
    if q:
        internships = internships.filter(Q(title__icontains=q) | Q(company__company_name__icontains=q))
    if type_filter:
        internships = internships.filter(internship_type=type_filter)
    if location:
        internships = internships.filter(location__icontains=location)
        
    context = {
        'internships': internships,
        'search_query': q,
        'selected_type': type_filter,
        'selected_location': location,
    }
    return render(request, 'students/browse_internships.html', context)

@login_required
@student_required
def internship_detail(request, pk):
    internship = get_object_or_404(Internship, pk=pk, is_approved=True, is_active=True, company__is_verified=True)
    profile = request.user.student_profile
    has_applied = Application.objects.filter(student=profile, internship=internship).exists()
    return render(request, 'students/internship_detail.html', {
        'internship': internship,
        'has_applied': has_applied,
        'profile': profile,
    })

@login_required
@student_required
def apply_internship(request, pk):
    internship = get_object_or_404(Internship, pk=pk, is_approved=True, is_active=True, company__is_verified=True)
    profile = request.user.student_profile

    if not profile.is_complete:
        missing = ', '.join(profile.missing_fields)
        messages.warning(request, f'⚠️ Please complete your profile before applying. Missing: {missing}.')
        return redirect('students:edit_profile')
    
    if Application.objects.filter(student=profile, internship=internship).exists():
        messages.warning(request, 'You have already applied for this internship.')
        return redirect('students:my_applications')
        
    if internship.application_deadline < date.today():
        messages.error(request, 'The application deadline for this internship has passed.')
        return redirect('students:browse_internships')
        
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.student = profile
            application.internship = internship
            application.save()
            messages.success(request, 'Your application has been submitted successfully!')
            return redirect('students:my_applications')
    else:
        form = ApplicationForm()
    
    return render(request, 'students/apply_internship.html', {'form': form, 'internship': internship})

@login_required
@student_required
def my_applications(request):
    applications = request.user.student_profile.applications.select_related('internship__company__user').order_by('-applied_at')
    return render(request, 'students/my_applications.html', {'applications': applications})

@login_required
@student_required
def notifications(request):
    """List all notifications for the student."""
    notifications_list = request.user.notifications.select_related('application__internship__company').all()
    unread_count = notifications_list.filter(is_read=False).count()
    return render(request, 'students/notifications.html', {
        'notifications': notifications_list,
        'unread_count': unread_count,
    })

@login_required
@student_required
def mark_notification_read(request, pk):
    """Mark a single notification as read."""
    if request.method == 'POST':
        notification = get_object_or_404(Notification, pk=pk, user=request.user)
        notification.is_read = True
        notification.save()
    return redirect('students:notifications')

@login_required
@student_required
def mark_all_notifications_read(request):
    """Mark all of the student's notifications as read."""
    if request.method == 'POST':
        request.user.notifications.filter(is_read=False).update(is_read=True)
    return redirect('students:notifications')
