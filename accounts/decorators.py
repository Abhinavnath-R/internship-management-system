from django.contrib.auth.decorators import user_passes_test

def admin_required(function=None):
    def check(user):
        return user.is_authenticated and user.role == 'admin'
    actual_decorator = user_passes_test(check, login_url='/accounts/login/')
    if function:
        return actual_decorator(function)
    return actual_decorator

def student_required(function=None):
    def check(user):
        return user.is_authenticated and user.role == 'student'
    actual_decorator = user_passes_test(check, login_url='/accounts/login/')
    if function:
        return actual_decorator(function)
    return actual_decorator

def company_required(function=None):
    def check(user):
        return user.is_authenticated and user.role == 'company'
    actual_decorator = user_passes_test(check, login_url='/accounts/login/')
    if function:
        return actual_decorator(function)
    return actual_decorator
