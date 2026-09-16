from django.db import models
from django.conf import settings

# companies/models.py
class CompanyProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='company_profile')
    company_name = models.CharField(max_length=200)
    industry = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.company_name
    
    @property
    def profile_completion(self):
        fields = ['company_name', 'industry', 'website', 'location', 'description', 'contact_email', 'contact_phone']
        filled = sum(1 for f in fields if getattr(self, f))
        return int((filled / len(fields)) * 100)


class Internship(models.Model):
    TYPE_CHOICES = (
        ('remote', 'Remote'),
        ('onsite', 'On-site'),
        ('hybrid', 'Hybrid'),
    )
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='internships')
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    location = models.CharField(max_length=200)
    internship_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    duration = models.CharField(max_length=50)
    stipend = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    positions_available = models.IntegerField(default=1)
    application_deadline = models.DateField()
    is_approved = models.BooleanField(default=True, help_text='Internships go live immediately when posted')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} at {self.company.company_name}"
    
    @property
    def is_expired(self):
        from django.utils import timezone
        return self.application_deadline < timezone.now().date()
    
    @property
    def total_applications(self):
        return self.applications.count()

    @property
    def requirements_list(self):
        """Return requirements as a list of items, one per line, for bulleted display."""
        items = []
        for line in self.requirements.splitlines():
            line = line.strip()
            if not line:
                continue
            # Strip common bullet markers if the company typed them manually
            for marker in ('- ', '• ', '* ', '· ', '– '):
                if line.startswith(marker):
                    line = line[len(marker):].strip()
                    break
            if line:
                items.append(line)
        return items
