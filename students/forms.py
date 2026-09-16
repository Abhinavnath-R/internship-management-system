from django import forms
from django.core.exceptions import ValidationError
from .models import StudentProfile, Application

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['first_name', 'last_name', 'phone', 'university', 'degree', 'major', 'graduation_year', 'gpa', 'skills', 'bio', 'resume', 'profile_picture', 'linkedin_url', 'github_url']
        widgets = {
            'skills': forms.Textarea(attrs={'rows': 3}),
            'bio': forms.Textarea(attrs={'rows': 3}),
            'resume': forms.FileInput(),
            'profile_picture': forms.FileInput(),
            'graduation_year': forms.NumberInput(),
            'gpa': forms.NumberInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume:
            if resume.size > 5 * 1024 * 1024:
                raise ValidationError("File size must be under 5MB.")
        return resume

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Write a brief cover letter explaining why you are a good fit for this internship...',
                'class': 'form-control'
            })
        }
