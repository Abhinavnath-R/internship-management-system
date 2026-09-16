from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('', views.dashboard, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('internships/', views.browse_internships, name='browse_internships'),
    path('internships/<int:pk>/', views.internship_detail, name='internship_detail'),
    path('internships/<int:pk>/apply/', views.apply_internship, name='apply_internship'),
    path('applications/', views.my_applications, name='my_applications'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/<int:pk>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/read-all/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
]
