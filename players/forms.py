from django import forms
from .models import Player, Opportunity, Application, CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import datetime


# Player Form
class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = [
            'name', 'age', 'position', 'height', 'location', 'skill_level',
            'scholarship_interest', 'achievements', 'profile_pic', 'contact_email',
            'availability', 'preferred_opportunities'
        ]
        widgets = {
            'achievements': forms.Textarea(attrs={'rows': 3, 'placeholder': 'List notable achievements here'}),
            'preferred_opportunities': forms.CheckboxSelectMultiple(),
        }

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 10 or age > 35:
            raise ValidationError("Age must be between 10 and 35 for eligibility.")
        return age

    def clean_height(self):
        height = self.cleaned_data.get('height')
        if height < 100 or height > 250:
            raise ValidationError("Height must be between 100 cm and 250 cm.")
        return height

    def clean_contact_email(self):
        contact_email = self.cleaned_data.get('contact_email')
        if contact_email and not contact_email.endswith('@example.com'):
            raise ValidationError("Please use a valid email address (e.g., ending with '@example.com').")
        return contact_email


# Opportunity Form
class OpportunityForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields = [
            'title', 'description', 'location', 'scholarship_type', 'skill_requirements',
            'basketball_program', 'application_deadline', 'contact_email', 'link'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Provide a detailed description of the opportunity'}),
            'application_deadline': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_application_deadline(self):
        deadline = self.cleaned_data.get('application_deadline')
        if deadline and deadline < datetime.date.today():
            raise ValidationError("The application deadline must be in the future.")
        return deadline

    def clean_link(self):
        link = self.cleaned_data.get('link')
        if not link.startswith('http://') and not link.startswith('https://'):
            raise ValidationError("Please provide a valid URL starting with 'http://' or 'https://'.")
        return link


# Application Form
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['opportunity', 'status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_status(self):
        status = self.cleaned_data.get('status')
        if status not in ['Pending', 'Accepted', 'Rejected']:
            raise ValidationError("Invalid status value.")
        return status


# Custom User Creation Form for Registration
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise ValidationError("Passwords do not match.")
        return password2
