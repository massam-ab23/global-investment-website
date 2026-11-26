from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from projects.models import Activity
from django.utils.translation import gettext as _
from django.conf import settings
from django.utils.translation import get_language
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from .models import CustomUser  

def register(request):
    """Handles user registration"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def custom_login(request):
    """Custom login view allowing admin to log in with either email or username, while visitors use only email"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Check if input is an email
            if '@' in username_or_email:
                try:
                    user = User.objects.get(email=username_or_email)
                    user = authenticate(request, username=user.username, password=password)
                except User.DoesNotExist:
                    user = None
            else:
                user = authenticate(request, username=username_or_email, password=password)

            if user is not None:
                login(request, user)
                return redirect('landing')  
            else:
                form.add_error(None, _("Invalid login credentials."))
    else:
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})

@login_required
def create_project(request):
    """Handles project creation (yet to be implemented)"""
    pass

@login_required
def profile(request):
    """Displays user profile along with their recent activities"""
    activities = Activity.objects.filter(user=request.user).order_by('-timestamp')[:10]  
    return render(request, 'users/profile.html', {
        'user': request.user,
        'activities': activities,
    })

@login_required
def edit_profile(request):
    """Allows users to edit their profile"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user.profile)
    return render(request, 'users/edit_profile.html', {'form': form})

def some_view(request):
    """Example of text translation usage"""
    translated_text = _("This text will be translated.")
    return render(request, "template.html", {"translated_text": translated_text})

def language_selection(request):
    """Handles language selection for the site"""
    current_language_code = get_language()
    current_language_name = dict(settings.LANGUAGES).get(current_language_code, "Language")
    return render(request, 'language_selection.html', {
        'languages': settings.LANGUAGES,
        'current_language_name': current_language_name
    })

def public_profile(request, username):
    user = get_object_or_404(CustomUser, username=username)
    return render(request, 'users/public_profile.html', {'user_profile': user})
