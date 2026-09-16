import uuid
from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator

def resume_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    return f'resumes/student_{instance.user.id}/{uuid.uuid4()}.{ext}'

class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    university = models.CharField(max_length=200, blank=True)
    degree = models.CharField(max_length=100, blank=True)
    major = models.CharField(max_length=100, blank=True)
    graduation_year = models.IntegerField(null=True, blank=True)
    gpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    skills = models.TextField(blank=True, help_text='Comma-separated skills')
    bio = models.TextField(blank=True)
    resume = models.FileField(
        upload_to=resume_upload_path,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])]
    )
    profile_picture = models.ImageField(upload_to='profile_pics/students/', blank=True, null=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user.username})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.user.username
    
    @property
    def profile_completion(self):
        fields = ['first_name', 'last_name', 'phone', 'university', 'degree', 'major', 'graduation_year', 'skills', 'bio', 'resume']
        filled = sum(1 for f in fields if getattr(self, f))
        return int((filled / len(fields)) * 100)

    @property
    def is_complete(self):
        """Check if the profile has all required fields to apply for internships."""
        required_fields = ['first_name', 'last_name', 'phone', 'university', 'degree', 'major', 'graduation_year']
        return all(getattr(self, f) for f in required_fields)

    @property
    def missing_fields(self):
        """Return a list of missing required field names for display."""
        field_labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'phone': 'Phone Number',
            'university': 'University',
            'degree': 'Degree',
            'major': 'Major',
            'graduation_year': 'Graduation Year',
        }
        missing = [field_labels[f] for f in field_labels if not getattr(self, f)]
        return missing


class Application(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('shortlisted', 'Shortlisted'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='applications')
    internship = models.ForeignKey('companies.Internship', on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'internship')
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.student.full_name} -> {self.internship.title} ({self.status})"


class Notification(models.Model):
    """In-app notification for students when their application status changes."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} -> {self.user.username}"
