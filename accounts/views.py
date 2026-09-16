from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, StudentRegistrationForm, CompanyRegistrationForm

def home(request):
    if request.user.is_authenticated:
        return role_redirect(request)
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('accounts:role_redirect')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('accounts:home')

def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            try:
                from students.models import StudentProfile
                StudentProfile.objects.create(user=user)
            except ImportError:
                pass
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('students:dashboard')
    else:
        form = StudentRegistrationForm()
    return render(request, 'accounts/register_student.html', {'form': form})

def register_company(request):
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            try:
                from companies.models import CompanyProfile
                CompanyProfile.objects.create(user=user, company_name=form.cleaned_data['company_name'], contact_email=form.cleaned_data['email'])
            except ImportError:
                pass
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('companies:dashboard')
    else:
        form = CompanyRegistrationForm()
    return render(request, 'accounts/register_company.html', {'form': form})

@login_required
def role_redirect(request):
    if request.user.role == 'admin':
        return redirect('dashboard:admin_dashboard')
    elif request.user.role == 'student':
        return redirect('students:dashboard')
    elif request.user.role == 'company':
        return redirect('companies:dashboard')
    return redirect('accounts:home')
