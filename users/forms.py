from django import forms 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import CustomUser
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Check if the email already exists in the database
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'bio', 'profile_picture', 'country', 'is_premium']

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Email address",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'})
    )

    def clean_username(self):
        username_or_email = self.cleaned_data.get('username')

        # Check if the user logging in is an admin
        if username_or_email == "your_admin_username":  # Replace with actual admin username
            return username_or_email  # Allow username login for admin

        # Check if it's an email
        if "@" in username_or_email:
            try:
                user = User.objects.get(email=username_or_email)
                return user.username  # Convert email to username for authentication
            except User.DoesNotExist:
                raise ValidationError("No account found with this email.")
        
        # If not admin and not email, reject login
        raise ValidationError("Visitors must use an email address.")
