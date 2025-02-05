from django import forms
from .models import Business
from .choices import (
    STATE_CHOICES, TITLE_CHOICES, ENTITY_CHOICES, CREDIT_CHOICES,
    PERSONAL_INCOME_CHOICES, MONTH_CHOICES, YEAR_CHOICES, INDUSTRY_CHOICES,
    AMOUNT_CHOICES
)

class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = [
            'business_legal_name', 'first_name', 'last_name', 'business_email', 'phone',
            'address', 'city', 'state', 'zip_code', 'business_phone', 'ein',
            'month_started', 'year_started', 'industry_focus', 'business_type',
            'domain_name', 'gross_monthly_revenue', 'total_monthly_credit_sales',
            'other_income', 'current_purchase_amount', 'value_of_other_equipment',
            'experian', 'transunion', 'equifax', 'judgments', 'bankruptcy', 'personal_income'
        ]
        widgets = {
            'business_legal_name': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-400',
                'placeholder': 'Business Legal Name',
                'required': True,
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-400',
                'placeholder': 'First Name',
                'required': True,
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-400',
                'placeholder': 'Last Name',
                'required': True,
            }),
            'business_email': forms.EmailInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-400',
                'placeholder': 'Contact Email',
                'required': True,
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-400',
                'placeholder': 'Contact Phone Number',
                'required': True,
            }),
            'address': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-400',
                'placeholder': 'Business Address',
                'required': True,
            }),
            'city': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-400',
                'placeholder': 'City',
                'required': True,
            }),
            'state': forms.Select(choices=STATE_CHOICES, attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-400',
                'required': True,
            }),
            'zip_code': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-400',
                'placeholder': 'Zip Code',
                'required': True,
            }),
            'business_phone': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-400',
                'placeholder': 'Business Phone Number',
                'required': True,
            }),
            'ein': forms.RadioSelect(choices=[('yes', 'Yes'), ('no', 'No')], attrs={
                'class': 'mr-2',
                'required': True,
            }),
            'month_started': forms.Select(choices=MONTH_CHOICES, attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-400',
            }),
            'year_started': forms.Select(choices=YEAR_CHOICES, attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-400',
            }),
            'industry_focus': forms.Select(choices=INDUSTRY_CHOICES, attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-400',
            }),
            'business_type': forms.Select(choices=ENTITY_CHOICES, attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-400',
            }),
            'domain_name': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-400',
                'placeholder': 'Enter without http:// or www',
            }),
            'gross_monthly_revenue': forms.Select(choices=AMOUNT_CHOICES, attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-400',
            }),
            'total_monthly_credit_sales': forms.Select(choices=AMOUNT_CHOICES, attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-400',
            }),
            'other_income': forms.Select(choices=AMOUNT_CHOICES, attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-400',
            }),
            'current_purchase_amount': forms.Select(choices=AMOUNT_CHOICES, attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-400',
            }),
            'value_of_other_equipment': forms.Select(choices=AMOUNT_CHOICES, attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-400',
            }),
            'experian': forms.Select(choices=CREDIT_CHOICES, attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-400',
            }),
            'transunion': forms.Select(choices=CREDIT_CHOICES, attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-400',
            }),
            'equifax': forms.Select(choices=CREDIT_CHOICES, attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-400',
            }),
            'judgments': forms.RadioSelect(choices=[('yes', 'Yes'), ('no', 'No')], attrs={
                'class': 'mr-2',
                'required': True,
            }),
            'bankruptcy': forms.RadioSelect(choices=[('yes', 'Yes'), ('no', 'No')], attrs={
                'class': 'mr-2',
                'required': True,
            }),
            'personal_income': forms.Select(choices=PERSONAL_INCOME_CHOICES, attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-400',
            }),
        }
