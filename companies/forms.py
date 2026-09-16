from django import forms
from django.core.exceptions import ValidationError
from datetime import date
from .models import CompanyProfile, Internship

class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ['company_name', 'industry', 'website', 'location', 'description', 'logo', 'contact_email', 'contact_phone']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'logo': forms.FileInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class InternshipForm(forms.ModelForm):
    class Meta:
        model = Internship
        fields = ['title', 'description', 'requirements', 'location', 'internship_type', 'duration', 'stipend', 'positions_available', 'application_deadline']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'requirements': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Enter each requirement on a new line, e.g.\n- Bachelor\'s degree in Computer Science\n- Proficiency in Python and Django\n- Good communication skills'}),
            'application_deadline': forms.DateInput(attrs={'type': 'date'}),
            'stipend': forms.NumberInput(),
            'positions_available': forms.NumberInput(),
            'internship_type': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_application_deadline(self):
        deadline = self.cleaned_data.get('application_deadline')
        if deadline and deadline < date.today():
            raise ValidationError('Deadline must be in the future')
        return deadline
