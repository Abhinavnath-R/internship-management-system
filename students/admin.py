from django.contrib import admin
from .models import StudentProfile, Application, Notification

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'university', 'major', 'graduation_year']
    list_filter = ['university', 'major']
    search_fields = ['first_name', 'last_name', 'user__username']

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['student', 'internship', 'status', 'applied_at']
    list_filter = ['status']
    search_fields = ['student__first_name', 'internship__title']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['user__username', 'title', 'message']
    readonly_fields = ['user', 'application', 'title', 'message', 'is_read', 'created_at']
