from django import forms
from django.contrib.auth.models import User
from .models import AccountInfo,OtherInfo
from django.core.exceptions import ValidationError
from buisness.models import ContactInfo
class SignUpForm(forms.ModelForm):
    username=forms.CharField(max_length=15,label="User Name")
    email=forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput,label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match.")

        return cleaned_data

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

class AccountInfoForm(forms.ModelForm):
    class Meta:
        model = AccountInfo
        fields = ['allow_bonus_vendors_access', 'registration_completed']

class OtherInfoForm(forms.ModelForm):
    class Meta:
        model = OtherInfo
        fields = ['paid_user', 'status']

class ContactInfoForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = ['company', 'first_name', 'last_name', 'phone', 'address', 'city', 'state', 'zip_code', 'email']
