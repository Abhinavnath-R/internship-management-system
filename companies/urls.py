
# companies/urls.py
from django.urls import path
from . import views

app_name = 'companies'

urlpatterns = [
    # Main pages
    path('dashboard/', views.company_dashboard, name='dashboard'),
    path('profile/', views.company_profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('post-internship/', views.post_internship, name='post_internship'),
    path('my-internships/', views.my_internships, name='my_internships'),
    
    # Internship management
    path('internship/<int:internship_id>/applicants/', views.view_applicants, name='view_applicants'),
    path('internship/<int:internship_id>/edit/', views.edit_internship, name='edit_internship'),
    path('internship/<int:internship_id>/delete/', views.delete_internship, name='delete_internship'),
    path('application/<int:application_id>/update-status/', views.update_application_status, name='update_application_status'),
    
    # Verification URLs
    path('debug-verification/', views.debug_verification, name='debug_verification'),
    path('quick-verify/', views.quick_verify, name='quick_verify'),
]