# companies/views.py - ADD THESE FUNCTIONS
from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from .models import CompanyProfile, Internship
from .forms import CompanyProfileForm, InternshipForm
from students.models import Application, Notification
import logging

logger = logging.getLogger(__name__)

# UPDATE YOUR EXISTING DASHBOARD VIEW
@login_required
@never_cache
def company_dashboard(request):
    try:
        profile = request.user.company_profile
        
        # Debug print (shows in terminal)
        print(f"DEBUG: {profile.company_name} - Verified: {profile.is_verified}")
        
        internships = Internship.objects.filter(company=profile)
        applications = Application.objects.filter(internship__company=profile)
        
        context = {
            'profile': profile,
            'is_verified': profile.is_verified,
            'total_internships': internships.count(),
            'active_internships': internships.filter(is_active=True, application_deadline__gte=date.today()).count(),
            'total_applicants': applications.count(),
            'pending_applications': applications.filter(status='pending').count(),
            'recent_applications': applications.select_related('student__user', 'internship').order_by('-applied_at')[:5],
        }
        
        return render(request, 'companies/dashboard.html', context)
        
    except CompanyProfile.DoesNotExist:
        return render(request, 'companies/setup_profile.html', {
            'error': 'Please complete your company profile first.'
        })

# ADD THIS DEBUG VIEW
@login_required
def debug_verification(request):
    """Debug endpoint to check verification status"""
    try:
        profile = request.user.company_profile
        return JsonResponse({
            'company_id': profile.id,
            'company_name': profile.company_name,
            'is_verified': profile.is_verified,
            'is_verified_type': str(type(profile.is_verified)),
            'updated_at': str(profile.updated_at),
            'user_id': request.user.id,
            'user_is_authenticated': request.user.is_authenticated,
            'all_companies': [
                {
                    'id': c.id,
                    'name': c.company_name,
                    'verified': c.is_verified,
                    'updated': str(c.updated_at)
                }
                for c in CompanyProfile.objects.all()
            ]
        })
    except CompanyProfile.DoesNotExist:
        return JsonResponse({
            'error': 'No company profile found',
            'user_id': request.user.id,
            'user_email': request.user.email,
        }, status=404)

# ADD THIS QUICK VERIFY VIEW
@login_required
def quick_verify(request):
    """Quick verify the company (for testing)"""
    try:
        profile = request.user.company_profile
        profile.is_verified = True
        profile.updated_at = timezone.now()
        profile.save()
        messages.success(request, f'✅ {profile.company_name} verified successfully!')
    except CompanyProfile.DoesNotExist:
        messages.error(request, 'Company profile not found')
    return redirect('companies:dashboard')

# companies/views.py - ADD THESE FUNCTIONS

@login_required
def company_profile(request):
    """Company profile page"""
    try:
        profile = request.user.company_profile
        return render(request, 'companies/profile.html', {'profile': profile})
    except CompanyProfile.DoesNotExist:
        return redirect('companies:dashboard')

@login_required
def post_internship(request):
    """Post a new internship"""
    try:
        profile = request.user.company_profile
        
        if not profile.is_verified:
            messages.warning(request, '⚠️ Your company has not been verified yet. Please wait for admin approval before posting internships.')
            return redirect('companies:dashboard')
        
        if request.method == 'POST':
            form = InternshipForm(request.POST)
            if form.is_valid():
                internship = form.save(commit=False)
                internship.company = profile
                internship.is_approved = True  # Goes live immediately, no admin approval needed
                internship.save()
                messages.success(request, '✅ Internship posted successfully! It is now live and visible to students.')
                return redirect('companies:my_internships')
        else:
            form = InternshipForm()
        
        return render(request, 'companies/post_internship.html', {'form': form, 'profile': profile})
        
    except CompanyProfile.DoesNotExist:
        messages.error(request, 'Company profile not found.')
        return redirect('companies:dashboard')

@login_required
def my_internships(request):
    """List company's internships with All / Active / Inactive filter tabs"""
    try:
        profile = request.user.company_profile
        internships = Internship.objects.filter(company=profile)
        
        filter_status = request.GET.get('status', '')
        today = date.today()
        
        if filter_status == 'active':
            # Active = live internships (active and not yet expired)
            internships = internships.filter(is_active=True, application_deadline__gte=today)
        elif filter_status == 'inactive':
            # Inactive = inactive OR expired internships
            internships = internships.filter(Q(is_active=False) | Q(application_deadline__lt=today))
        
        return render(request, 'companies/my_internships.html', {
            'profile': profile,
            'internships': internships,
            'filter_status': filter_status,
        })
    except CompanyProfile.DoesNotExist:
        return redirect('companies:dashboard')

@login_required
def edit_profile(request):
    """Edit company profile"""
    try:
        profile = request.user.company_profile
        
        if request.method == 'POST':
            form = CompanyProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, '✅ Profile updated successfully!')
                return redirect('companies:profile')
        else:
            form = CompanyProfileForm(instance=profile)
        
        return render(request, 'companies/edit_profile.html', {'form': form, 'profile': profile})
        
    except CompanyProfile.DoesNotExist:
        messages.error(request, 'Company profile not found.')
        return redirect('companies:dashboard')

    # companies/views.py - Add this function

@login_required
def view_applicants(request, internship_id):
    """View applicants for a specific internship"""
    try:
        profile = request.user.company_profile
        internship = Internship.objects.get(id=internship_id, company=profile)
        
        applications = Application.objects.filter(internship=internship).select_related('student__user')
        
        context = {
            'profile': profile,
            'internship': internship,
            'applications': applications,
        }
        return render(request, 'companies/view_applicants.html', context)
        
    except Internship.DoesNotExist:
        messages.error(request, 'Internship not found.')
        return redirect('companies:my_internships')

    # companies/views.py - Add this function

@login_required
def edit_internship(request, internship_id):
    """Edit an existing internship"""
    try:
        profile = request.user.company_profile
        internship = Internship.objects.get(id=internship_id, company=profile)
        
        if request.method == 'POST':
            form = InternshipForm(request.POST, instance=internship)
            if form.is_valid():
                form.save()
                messages.success(request, '✅ Internship updated successfully!')
                return redirect('companies:my_internships')
        else:
            form = InternshipForm(instance=internship)
        
        return render(request, 'companies/edit_internship.html', {'form': form, 'profile': profile, 'internship': internship})
        
    except Internship.DoesNotExist:
        messages.error(request, 'Internship not found.')
        return redirect('companies:my_internships')


@login_required
def update_application_status(request, application_id):
    """Update the status of an application and notify the student"""
    if request.method == 'POST':
        new_status = request.POST.get('status', '')
        valid_statuses = ['reviewed', 'shortlisted', 'accepted', 'rejected']
        
        if new_status not in valid_statuses:
            messages.error(request, 'Invalid status.')
            return redirect('companies:my_internships')
        
        try:
            profile = request.user.company_profile
            application = Application.objects.get(
                id=application_id,
                internship__company=profile
            )
            if new_status == application.status:
                messages.info(request, f'Application is already marked as {new_status}.')
                return redirect('companies:view_applicants', internship_id=application.internship.id)
            
            application.status = new_status
            application.save()
            
            # Notify the student about the status change
            notify_application_status(application)
            
            messages.success(request, f'Application status updated to {new_status}. Student notified.')
            return redirect('companies:view_applicants', internship_id=application.internship.id)
            
        except Application.DoesNotExist:
            messages.error(request, 'Application not found.')
            return redirect('companies:my_internships')
    
    return redirect('companies:my_internships')


def notify_application_status(application):
    """Create an in-app notification for the student based on the application status."""
    internship = application.internship
    company_name = internship.company.company_name
    student_user = application.student.user
    
    messages_map = {
        'reviewed': (
            'Application Reviewed',
            f'Your application for "{internship.title}" at {company_name} has been marked as reviewed. The company will get back to you with the next steps soon.'
        ),
        'shortlisted': (
            "You've Been Shortlisted! 🎉",
            f'Congratulations! You have been shortlisted for "{internship.title}" at {company_name}. Further action will be taken soon — please wait for the company to contact you. Keep an eye on your inbox and this portal for updates.'
        ),
        'accepted': (
            'Application Accepted! 🎉',
            f'Great news! Your application for "{internship.title}" at {company_name} has been accepted. The company will reach out with the next steps.'
        ),
        'rejected': (
            'Application Update',
            f'Unfortunately, your application for "{internship.title}" at {company_name} was not successful this time. Don\'t get discouraged — keep exploring new opportunities on the portal.'
        ),
    }
    
    title, message = messages_map.get(application.status, ('Application Update', 'Your application status has been updated.'))
    
    Notification.objects.create(
        user=student_user,
        application=application,
        title=title,
        message=message,
    )


@login_required
def delete_internship(request, internship_id):
    """Delete an internship"""
    try:
        profile = request.user.company_profile
        internship = Internship.objects.get(id=internship_id, company=profile)
        
        if request.method == 'POST':
            internship.delete()
            messages.success(request, '🗑️ Internship deleted successfully!')
        else:
            messages.error(request, 'Invalid request method.')
        
        return redirect('companies:my_internships')
        
    except Internship.DoesNotExist:
        messages.error(request, 'Internship not found.')
        return redirect('companies:my_internships')