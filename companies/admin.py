# companies/admin.py
from django.contrib import admin
from django.utils import timezone
from django.contrib import messages
from .models import CompanyProfile, Internship

@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    # Make sure these fields exist in your model
    list_display = ['id', 'company_name', 'industry', 'is_verified', 'user', 'created_at']
    list_filter = ['is_verified', 'industry', 'created_at']
    search_fields = ['company_name', 'industry', 'user__email', 'contact_email']
    readonly_fields = ['created_at', 'updated_at', 'user']
    
    # Custom actions for verification
    actions = ['verify_companies', 'unverify_companies']
    
    def verify_companies(self, request, queryset):
        updated = queryset.update(
            is_verified=True,
            updated_at=timezone.now()
        )
        self.message_user(
            request, 
            f'✅ Successfully verified {updated} company(s).',
            messages.SUCCESS
        )
    verify_companies.short_description = '✅ Verify selected companies'
    
    def unverify_companies(self, request, queryset):
        updated = queryset.update(
            is_verified=False,
            updated_at=timezone.now()
        )
        self.message_user(
            request, 
            f'⚠️ Unverified {updated} company(s).',
            messages.WARNING
        )
    unverify_companies.short_description = '⚠️ Unverify selected companies'
    
    # Better organization in admin
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'company_name', 'industry')
        }),
        ('Contact Details', {
            'fields': ('contact_email', 'contact_phone', 'website')
        }),
        ('Location & Description', {
            'fields': ('location', 'description')
        }),
        ('Media', {
            'fields': ('logo',),
            'classes': ('collapse',)
        }),
        ('Verification Status', {
            'fields': ('is_verified',),
            'description': 'Check this box to verify the company'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'company', 'is_active', 'application_deadline']
    list_filter = ['is_active', 'internship_type', 'company']
    search_fields = ['title', 'company__company_name', 'description']
    readonly_fields = ['created_at', 'updated_at']