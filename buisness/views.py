from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
from .models import Business, Client
from serviceprovider.models import CustomUser
from clients.models import AccountInfo
from django.contrib.auth.models import User  # Import the base User model
from django.contrib.auth import login
from .choices import (
    STATE_CHOICES, TITLE_CHOICES, ENTITY_CHOICES, CREDIT_CHOICES,
    PERSONAL_INCOME_CHOICES, MONTH_CHOICES, YEAR_CHOICES, INDUSTRY_CHOICES,
    AMOUNT_CHOICES
)
def register_business(request):
    if request.method == 'POST':
        business_email = request.POST.get('business_mail')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        

        # Check if a CustomUser with the provided email already exists
        if CustomUser.objects.filter(email=business_email).exists():
            messages.error(request, "A user with this email address has already registered. Please use a different email.")
            return redirect('business_registration')

        # Check if a Client with the provided email already exists
        if Client.objects.filter(email=business_email).exists():
            messages.error(request, "A client with this email address already exists.")
            return redirect('business_registration')

        # Check if a Business with the provided email already exists
        if Business.objects.filter(business_email=business_email).exists():
            messages.error(request, "A business with this email address is already registered.")
            return redirect('business_registration')

        try:
            # Create the CustomUser
            user = CustomUser.objects.create_user(
                username=business_email,  # Set email as the username
                password='client@123',  # Default password
                email=business_email,
                first_name=first_name,  # Set first name from form
                last_name=last_name,    # Set last name from form
                user_type='client'      # Ensure user_type is 'client'
            )
            
            # Create the AccountInfo for the user
            account_info = AccountInfo.objects.create(
                user=user,
                last_login=None,  # Optionally, set last_login if needed
                allow_bonus_vendors_access=False  # Default value, can be adjusted
            )

            # Create the Client profile linked to the CustomUser
            client = Client.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                email=business_email,
                phone=request.POST.get('contact_phone'),
                
            )

            # Collect the business data from the form
            business_data = {
                'client': client,  # Link to the created client
                'business_legal_name': request.POST.get('business_legal_name'),
                'business_email': business_email,
                'business_phone': request.POST.get('business_phone'),
                'ein': request.POST.get('ein') == 'yes',
                'address':request.POST.get('business_address'),
                'city':request.POST.get('city'),
                'state':request.POST.get('state'),
                'zip_code':request.POST.get('zip_code'),
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

            # Validate the business legal name
            if not business_data['business_legal_name']:
                messages.error(request, "Business legal name is required.")
                return redirect('business_registration')

            # Create and save the business object
            business = Business(**business_data)
            business.save()

            # Log the user in
            login(request, user)

            # Ensure the user has a valid ID before redirecting
            if user.id is not None:
                messages.success(request, "Business registration successful. You are now logged in.")
                return redirect('clientindex', user_id=user.id)
            else:
                # If for any reason user.id is None, handle the error gracefully
                messages.error(request, "There was an issue with the user ID during registration.")
                return redirect('business_registration')

        except IntegrityError as e:
            messages.error(request, f"There was an integrity error during registration: {str(e)}")
            return redirect('business_registration')
        except Exception as e:
            messages.error(request, f"There was an unexpected error during registration: {str(e)}")
            return redirect('business_registration')

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

