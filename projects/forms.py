import re
import decimal
from django import forms
from django.core.exceptions import ValidationError
from projects.models import Project  
from django.contrib.auth import get_user_model
from .models import InvestmentApplication
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from django.contrib.auth.models import User
from .models import UserProfile


class ProjectForm(forms.ModelForm):
    """Form for creating a new project."""
    contact_information = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your email or phone number',
        }),
        help_text="Provide your email or phone number so we can contact you."
    )

    investment_required = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter investment amount (e.g., 100,000.00$)',
            'title': 'Format: 100,000.00$',
        })
    )

    class Meta:
        model = Project
        fields = ['title', 'description', 'sector', 'country', 'investment_required', 'contact_information']

    def clean_investment_required(self):
        raw_value = self.cleaned_data.get('investment_required', '')

        if not raw_value:
            raise ValidationError("This field is required.")

        try:
            cleaned_value = re.sub(r'[,\$]', '', str(raw_value))
            value = decimal.Decimal(cleaned_value)

            if value <= 0:
                raise ValidationError("Investment amount must be greater than zero.")
            return value
        except (ValueError, decimal.InvalidOperation):
            raise ValidationError("Enter a valid investment amount in the format 100,000.00$.")

class ApplyToInvestForm(forms.ModelForm):
    contact_information = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your email or phone number',
        }),
        help_text="Provide your email or phone number so we can contact you."
    )

    investment_required = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter investment amount (e.g., 100,000.00$)',
            'title': 'Format: 100,000.00$',
        })
    )

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta:
        model = InvestmentApplication
        fields = ['title', 'sector', 'country', 'investment_required', 'contact_information', 'message']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
            'sector': forms.Select(attrs={'class': 'form-select'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter country'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Why are you interested in this project?'}),
        }

    def clean_investment_required(self):
        raw_value = self.cleaned_data.get('investment_required', '')

        if not raw_value:
            raise forms.ValidationError("This field is required.")

        try:
            # Remove commas and dollar signs for validation
            cleaned_value = re.sub(r'[,\$]', '', str(raw_value))
            value = decimal.Decimal(cleaned_value)

            if value <= 0:
                raise forms.ValidationError("Investment amount must be greater than zero.")
            return value
        except (ValueError, decimal.InvalidOperation):
            raise forms.ValidationError("Enter a valid investment amount in the format 100,000.00$.")


class ProjectAdminForm(forms.ModelForm):
    investment_required = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            formatted_value = f"{self.instance.investment_required:,.2f}$"
            self.fields['investment_required'].initial = formatted_value

    def clean_investment_required(self):
        """Clean and validate the investment_required field."""
        raw_value = self.cleaned_data['investment_required']
        try:
            # Remove commas and dollar sign for validation
            cleaned_value = raw_value.replace(',', '').replace('$', '')
            return float(cleaned_value)
        except ValueError:
            raise forms.ValidationError("Enter a valid investment amount in the format 100,000.00$.")

    class Meta:
        model = Project
        fields = '__all__'


class CollaboratorInviteForm(forms.Form):
    email_or_username = forms.CharField(
        label="Collaborator's Email or Username",
        max_length=150,
        help_text="Enter the email or username of the collaborator you want to invite."
    )

    def clean_email_or_username(self):
        User = get_user_model()
        identifier = self.cleaned_data['email_or_username']
        try:
            user = User.objects.get(email=identifier) if '@' in identifier else User.objects.get(username=identifier)
        except User.DoesNotExist:
            raise forms.ValidationError("No user found with this email or username.")
        return user

class InvestmentApplicationForm(forms.ModelForm):
    class Meta:
        model = InvestmentApplication
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
        labels = {
            'message': 'Why are you interested in this project?',
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture', 'country', 'is_premium']
    
    def clean_country(self):
        country = self.cleaned_data.get('country')
        if not country:
            return "Not Specified"  
        return country
    
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())  
