from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from clients.views import is_client
from django.contrib import messages
from django.db import IntegrityError  # Import IntegrityError for specific error handling
from .models import Business
from .choices import (
    STATE_CHOICES, TITLE_CHOICES, ENTITY_CHOICES, CREDIT_CHOICES, 
    PERSONAL_INCOME_CHOICES, MONTH_CHOICES, YEAR_CHOICES, INDUSTRY_CHOICES, 
    AMOUNT_CHOICES
)
# @user_passes_test(is_client)
# @login_required
def register_business(request):
    if request.method == 'POST':
        user = request.user
        # Check if Business already exists for this user
        if hasattr(user, 'business'):
            messages.error(request, "Business information already exists for this account.")
            return redirect('clientindex')

        # Collect and validate form data
        business_data = {
            'user': user,
            'business_legal_name': request.POST.get('business_legal_name'),
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'business_email': request.POST.get('business_mail'),
            'phone': request.POST.get('contact_phone'),
            'address': request.POST.get('business_address'),
            'city': request.POST.get('city'),
            'state': request.POST.get('state'),
            'zip_code': request.POST.get('zip_code'),
            'business_phone': request.POST.get('business_phone'),
            'ein': request.POST.get('ein') == 'yes',
            'month_started': request.POST.get('month'),
            'year_started': request.POST.get('year'),
            'industry_focus': request.POST.get('industry_focus'),
            'business_type': request.POST.get('business_type'),
            'domain_name': request.POST.get('domain_name'),
            'gross_monthly_revenue': request.POST.get('gross_revenue'),
            'total_monthly_credit_sales': request.POST.get('credit_sales'),
            'other_income': request.POST.get('owed_amount'),
            'current_purchase_amount': request.POST.get('purchase_orders'),
            'value_of_other_equipment': request.POST.get('equipment_value'),
            'experian': request.POST.get('experian'),
            'transunion': request.POST.get('transunion'),
            'equifax': request.POST.get('equifax'),
            'judgments': request.POST.get('judgments') == 'yes',
            'bankruptcy': request.POST.get('bankruptcy') == 'yes',
            'personal_income': request.POST.get('personal_income'),
        }

        # Validate that required fields are not empty
        if not business_data['business_legal_name']:
            messages.error(request, "Business legal name is required.")
            return redirect('business_registration')

        # Create and save the Business object
        try:
            Business.objects.create(**business_data)
            messages.success(request, "Business registration successful.")
            return redirect('clientindex')
        except IntegrityError as e:
            messages.error(request, "There was an integrity error saving the business details.")
            return redirect('business_registration')
        except Exception as e:
            messages.error(request, "There was an unexpected error saving the business details.")
            return redirect('business_registration')

    # Render the form with choice options
    return render(request, 'clients/buisnessregistration.html', {
        "state_choices": STATE_CHOICES,
        "title_choices": TITLE_CHOICES,
        "entity_choices": ENTITY_CHOICES,
        "credit_choices": CREDIT_CHOICES,
        "income_choices": PERSONAL_INCOME_CHOICES,
        "month_choices": MONTH_CHOICES,
        "year_choices": YEAR_CHOICES,
        "industry_choices": INDUSTRY_CHOICES,
        "amount_choices": AMOUNT_CHOICES,
    })

