from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import admin_required
from accounts.models import User
from students.models import StudentProfile, Application
from companies.models import CompanyProfile, Internship
from django.db.models import Count, Q
from django.contrib import messages
import csv
from django.http import HttpResponse

@login_required
@admin_required
def admin_dashboard(request):
    total_students = User.objects.filter(role='student').count()
    total_companies = User.objects.filter(role='company').count()
    verified_companies = CompanyProfile.objects.filter(is_verified=True).count()
    unverified_companies = CompanyProfile.objects.filter(is_verified=False).count()
    
    context = {
        'total_students': total_students,
        'total_companies': total_companies,
        'verified_companies': verified_companies,
        'unverified_companies': unverified_companies,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)

@login_required
@admin_required
def manage_students(request):
    q = request.GET.get('q', '')
    students = StudentProfile.objects.select_related('user').annotate(
        total_applications=Count('applications')
    )
    if q:
        students = students.filter(
            Q(user__username__icontains=q) |
            Q(user__first_name__icontains=q) |
            Q(user__last_name__icontains=q) |
            Q(user__email__icontains=q) |
            Q(university__icontains=q) |
            Q(major__icontains=q) |
            Q(skills__icontains=q)
        )
    return render(request, 'dashboard/manage_students.html', {'students': students, 'search_query': q})

@login_required
@admin_required
def delete_student(request, pk):
    if request.method == 'POST':
        student = get_object_or_404(StudentProfile, pk=pk)
        student.user.delete()
        messages.success(request, 'Student deleted successfully.')
    return redirect('dashboard:manage_students')

@login_required
@admin_required
def manage_companies(request):
    q = request.GET.get('q', '')
    verified = request.GET.get('verified', '')
    companies = CompanyProfile.objects.select_related('user').annotate(
        total_internships=Count('internships')
    )
    if verified == 'yes':
        companies = companies.filter(is_verified=True)
    elif verified == 'no':
        companies = companies.filter(is_verified=False)
    if q:
        companies = companies.filter(
            Q(user__username__icontains=q) |
            Q(company_name__icontains=q) |
            Q(industry__icontains=q) |
            Q(contact_email__icontains=q) |
            Q(location__icontains=q)
        )
    return render(request, 'dashboard/manage_companies.html', {'companies': companies, 'search_query': q, 'verified': verified})

@login_required
@admin_required
def verify_company(request, pk):
    if request.method == 'POST':
        company = get_object_or_404(CompanyProfile, pk=pk)
        if company.is_verified:
            messages.error(request, 'Company is already verified. Use deactivate to make it inactive.')
        else:
            company.is_verified = True
            company.save()
            messages.success(request, f'{company.company_name} verified successfully.')
    return redirect('dashboard:manage_companies')

@login_required
@admin_required
def delete_company(request, pk):
    if request.method == 'POST':
        company = get_object_or_404(CompanyProfile, pk=pk)
        company.user.delete()
        messages.success(request, 'Company deleted successfully.')
    return redirect('dashboard:manage_companies')

@login_required
@admin_required
def manage_internships(request):
    filter_status = request.GET.get('status', '')
    internships = Internship.objects.select_related('company')
    
    today = date.today()
    
    if filter_status == 'active':
        # Active = live internships (active and not yet expired)
        internships = internships.filter(is_active=True, application_deadline__gte=today)
    elif filter_status == 'inactive':
        # Inactive = inactive OR expired internships
        internships = internships.filter(Q(is_active=False) | Q(application_deadline__lt=today))
        
    return render(request, 'dashboard/manage_internships.html', {'internships': internships, 'filter_status': filter_status})

@login_required
@admin_required
def delete_internship(request, pk):
    if request.method == 'POST':
        internship = get_object_or_404(Internship, pk=pk)
        internship.delete()
        messages.success(request, 'Internship deleted.')
    return redirect('dashboard:manage_internships')

@login_required
@admin_required
def toggle_internship_active(request, pk):
    """Toggle internship active status (moderation tool, not approval)"""
    if request.method == 'POST':
        internship = get_object_or_404(Internship, pk=pk)
        internship.is_active = not internship.is_active
        internship.save()
        status = 'activated' if internship.is_active else 'deactivated'
        messages.success(request, f'Internship {status} successfully.')
    return redirect('dashboard:manage_internships')

@login_required
@admin_required
def toggle_company_active(request, pk):
    """Toggle company user account active status"""
    if request.method == 'POST':
        company = get_object_or_404(CompanyProfile, pk=pk)
        if company.is_verified:
            company.user.is_active = not company.user.is_active
            company.user.save()
            status = 'activated' if company.user.is_active else 'deactivated'
            messages.success(request, f'{company.company_name} {status} successfully.')
        else:
            messages.error(request, 'Can only toggle active status on verified companies.')
    return redirect('dashboard:manage_companies')

@login_required
@admin_required
def view_student(request, pk):
    """View full student details"""
    student = get_object_or_404(StudentProfile.objects.select_related('user'), pk=pk)
    applications = Application.objects.filter(student=student).select_related('internship__company')
    
    total_apps = applications.count()
    pending_apps = applications.filter(status='pending').count()
    accepted_apps = applications.filter(status='accepted').count()
    rejected_apps = applications.filter(status='rejected').count()
    
    return render(request, 'dashboard/student_detail.html', {
        'student': student,
        'applications': applications,
        'total_apps': total_apps,
        'pending_apps': pending_apps,
        'accepted_apps': accepted_apps,
        'rejected_apps': rejected_apps,
    })


@login_required
@admin_required
def view_company(request, pk):
    """View full company details"""
    company = get_object_or_404(CompanyProfile.objects.select_related('user'), pk=pk)
    internships = Internship.objects.filter(company=company)
    
    total_apps = Application.objects.filter(internship__company=company).count()
    
    return render(request, 'dashboard/company_detail.html', {
        'company': company,
        'internships': internships,
        'total_internships': internships.count(),
        'total_applications': total_apps,
    })


@login_required
@admin_required
def view_internship(request, pk):
    """View full internship details"""
    internship = get_object_or_404(Internship.objects.select_related('company'), pk=pk)
    applications = Application.objects.filter(internship=internship).select_related('student__user')
    return render(request, 'dashboard/internship_detail.html', {
        'internship': internship,
        'applications': applications,
        'total_applicants': applications.count(),
    })


@login_required
@admin_required
def manage_applications(request):
    filter_status = request.GET.get('status', '')
    applications = Application.objects.select_related('student__user', 'internship__company')
    if filter_status:
        applications = applications.filter(status=filter_status)
    return render(request, 'dashboard/manage_applications.html', {'applications': applications, 'filter_status': filter_status})

@login_required
@admin_required
def reports(request):
    status_stats = Application.objects.values('status').annotate(count=Count('id')).order_by('status')
    top_companies = CompanyProfile.objects.annotate(app_count=Count('internships__applications')).order_by('-app_count')[:5]
    type_stats = Internship.objects.values('internship_type').annotate(count=Count('id')).order_by('internship_type')
    
    context = {
        'status_stats': status_stats,
        'top_companies': top_companies,
        'type_stats': type_stats,
    }
    return render(request, 'dashboard/reports.html', context)

@login_required
@admin_required
def export_report(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="applications_report.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Student', 'Email', 'Internship', 'Company', 'Status', 'Applied Date'])
    
    applications = Application.objects.select_related('student__user', 'internship__company').all()
    for app in applications:
        writer.writerow([
            app.student.user.get_full_name() or app.student.user.username,
            app.student.user.email,
            app.internship.title,
            app.internship.company.company_name,
            app.status,
            app.applied_at.strftime('%Y-%m-%d %H:%M')
        ])
        
    return response
