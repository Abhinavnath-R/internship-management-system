from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('students/', views.manage_students, name='manage_students'),
    path('students/<int:pk>/', views.view_student, name='view_student'),
    path('students/<int:pk>/delete/', views.delete_student, name='delete_student'),
    path('companies/', views.manage_companies, name='manage_companies'),
    path('companies/<int:pk>/', views.view_company, name='view_company'),
    path('companies/<int:pk>/verify/', views.verify_company, name='verify_company'),
    path('companies/<int:pk>/delete/', views.delete_company, name='delete_company'),
    path('internships/', views.manage_internships, name='manage_internships'),
    path('internships/<int:pk>/', views.view_internship, name='view_internship'),
    path('internships/<int:pk>/toggle-active/', views.toggle_internship_active, name='toggle_internship_active'),
    path('internships/<int:pk>/delete/', views.delete_internship, name='delete_internship'),
    path('companies/<int:pk>/toggle-active/', views.toggle_company_active, name='toggle_company_active'),
    path('applications/', views.manage_applications, name='manage_applications'),
    path('reports/', views.reports, name='reports'),
    path('reports/export/', views.export_report, name='export_report'),
]
