from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError  # Import IntegrityError for specific error handling
from .models import Business
from django.core.mail import send_mail
from django.conf import settings
from .models import Business,Client
from serviceprovider.models import CustomUser 
from .choices import (
    STATE_CHOICES, TITLE_CHOICES, ENTITY_CHOICES, CREDIT_CHOICES, 
    PERSONAL_INCOME_CHOICES, MONTH_CHOICES, YEAR_CHOICES, INDUSTRY_CHOICES, 
    AMOUNT_CHOICES
)

 # Ensure you import CustomUser
def register_business(request):
    if request.method == 'POST':
        # Retrieve the email from the form data
        business_email = request.POST.get('business_mail')
        
        # Check if a user with the provided email already exists
        if CustomUser.objects.filter(email=business_email).exists():
            messages.error(request, "A user with this email address has already registered. Please use a different email.")
            return redirect('business_registration')

        # Check if a business with the provided email already exists
        if Business.objects.filter(business_email=business_email).exists():
            messages.error(request, "A business with this email address is already registered.")
            return redirect('business_registration')

        # Create the CustomUser with the provided data
        user = CustomUser.objects.create_user(
            username=request.POST.get('first_name') + request.POST.get('last_name'),  # Combine first and last name
            password='temporary_password',  # A temporary password, can be changed later
            email=business_email
        )

        # Create or get the client based on the email
        client, created = Client.objects.get_or_create(email=business_email)

        # Collect the business data
        business_data = {
            'user': user,
            'business_legal_name': request.POST.get('business_legal_name'),
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'business_email': business_email,
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

        # Validate the business registration form
        if not business_data['business_legal_name']:
            messages.error(request, "Business legal name is required.")
            return redirect('business_registration')

        # Create and save the business object
        try:
            business = Business(
                user=user,
                client=client,
                business_legal_name=business_data['business_legal_name'],
                first_name=business_data['first_name'],
                last_name=business_data['last_name'],
                business_email=business_data['business_email'],
                phone=business_data['phone'],
                address=business_data['address'],
                city=business_data['city'],
                state=business_data['state'],
                zip_code=business_data['zip_code'],
                business_phone=business_data['business_phone'],
                ein=business_data['ein'],
                month_started=business_data['month_started'],
                year_started=business_data['year_started'],
                industry_focus=business_data['industry_focus'],
                business_type=business_data['business_type'],
                domain_name=business_data['domain_name'],
                gross_monthly_revenue=business_data['gross_monthly_revenue'],
                total_monthly_credit_sales=business_data['total_monthly_credit_sales'],
                other_income=business_data['other_income'],
                current_purchase_amount=business_data['current_purchase_amount'],
                value_of_other_equipment=business_data['value_of_other_equipment'],
                experian=business_data['experian'],
                transunion=business_data['transunion'],
                equifax=business_data['equifax'],
                judgments=business_data['judgments'],
                bankruptcy=business_data['bankruptcy'],
                personal_income=business_data['personal_income']
            )
            business.save()
            # send_welcome_email(user)  # Uncomment to send the email
            messages.success(request, "Business registration successful.")
            return redirect('login')
        except IntegrityError as e:
            messages.error(request, "There was an integrity error saving the business details.")
            return redirect('business_registration')
        except Exception as e:
            messages.error(request, f"There was an unexpected error saving the business details: {str(e)}")
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

# def send_welcome_email(user):
#     subject = "Your Business Account Details"
#     message = f"Hello {user.first_name},\n\nYour business account has been successfully registered.\n\n" \
#               f"Your login credentials are as follows:\n" \
#               f"Username: {user.username}\nPassword: temporary_password\n\n" \
#               "You can change your password after logging in.\n\n" \
#               "Best regards,\nThe Team"
    
#     send_mail(
#         subject,
#         message,
#         settings.DEFAULT_FROM_EMAIL,  # Default email from your settings.py
#         [user.email],
#         fail_silently=False,
#     )


# def register_business(request):
#     if request.method == 'POST':
#         # Collect form data
#         business_data = {
#             'business_legal_name': request.POST.get('business_legal_name'),
#             'first_name': request.POST.get('first_name'),
#             'last_name': request.POST.get('last_name'),
#             'business_email': request.POST.get('business_mail'),
#             'phone': request.POST.get('contact_phone'),
#             'address': request.POST.get('business_address'),
#             'city': request.POST.get('city'),
#             'state': request.POST.get('state'),
#             'zip_code': request.POST.get('zip_code'),
#             'business_phone': request.POST.get('business_phone'),
#             'ein': request.POST.get('ein') == 'yes',
#             'month_started': request.POST.get('month'),
#             'year_started': request.POST.get('year'),
#             'industry_focus': request.POST.get('industry_focus'),
#             'business_type': request.POST.get('business_type'),
#             'domain_name': request.POST.get('domain_name'),
#             'gross_monthly_revenue': request.POST.get('gross_revenue'),
#             'total_monthly_credit_sales': request.POST.get('credit_sales'),
#             'other_income': request.POST.get('owed_amount'),
#             'current_purchase_amount': request.POST.get('purchase_orders'),
#             'value_of_other_equipment': request.POST.get('equipment_value'),
#             'experian': request.POST.get('experian'),
#             'transunion': request.POST.get('transunion'),
#             'equifax': request.POST.get('equifax'),
#             'judgments': request.POST.get('judgments') == 'yes',
#             'bankruptcy': request.POST.get('bankruptcy') == 'yes',
#             'personal_income': request.POST.get('personal_income'),
#         }

#         # Validate that required fields are not empty
#         if not business_data['business_legal_name']:
#             messages.error(request, "Business legal name is required.")
#             return redirect('business_registration')

#         try:
#             # Create the Business object without user or client
#             Business.objects.create(**business_data)

#             # Redirect to the client dashboard (assuming it exists)
#             messages.success(request, "Business registration successful.")
#             return redirect('clientindex')  # Redirect to dashboard after registration

#         except IntegrityError as e:
#             messages.error(request, "There was an integrity error saving the business details.")
#             return redirect('business_registration')
#         except Exception as e:
#             messages.error(request, f"There was an unexpected error saving the business details: {e}")
#             return redirect('business_registration')

#     # Render the form with choice options
#     return render(request, 'clients/buisnessregistration.html', {
#         "state_choices": STATE_CHOICES,
#         "title_choices": TITLE_CHOICES,
#         "entity_choices": ENTITY_CHOICES,
#         "credit_choices": CREDIT_CHOICES,
#         "income_choices": PERSONAL_INCOME_CHOICES,
#         "month_choices": MONTH_CHOICES,
#         "year_choices": YEAR_CHOICES,
#         "industry_choices": INDUSTRY_CHOICES,
#         "amount_choices": AMOUNT_CHOICES,
#     })

# # @user_passes_test(is_client)
# # @login_required
# def register_business(request):
#     if request.method == 'POST':
#         user = request.user
#         # Check if Business already exists for this user
#         if hasattr(user, 'business'):
#             messages.error(request, "Business information already exists for this account.")
#             return redirect('clientindex')

#         # Collect and validate form data
#         business_data = {
#             'user': user,
#             'business_legal_name': request.POST.get('business_legal_name'),
#             'first_name': request.POST.get('first_name'),
#             'last_name': request.POST.get('last_name'),
#             'business_email': request.POST.get('business_mail'),
#             'phone': request.POST.get('contact_phone'),
#             'address': request.POST.get('business_address'),
#             'city': request.POST.get('city'),
#             'state': request.POST.get('state'),
#             'zip_code': request.POST.get('zip_code'),
#             'business_phone': request.POST.get('business_phone'),
#             'ein': request.POST.get('ein') == 'yes',
#             'month_started': request.POST.get('month'),
#             'year_started': request.POST.get('year'),
#             'industry_focus': request.POST.get('industry_focus'),
#             'business_type': request.POST.get('business_type'),
#             'domain_name': request.POST.get('domain_name'),
#             'gross_monthly_revenue': request.POST.get('gross_revenue'),
#             'total_monthly_credit_sales': request.POST.get('credit_sales'),
#             'other_income': request.POST.get('owed_amount'),
#             'current_purchase_amount': request.POST.get('purchase_orders'),
#             'value_of_other_equipment': request.POST.get('equipment_value'),
#             'experian': request.POST.get('experian'),
#             'transunion': request.POST.get('transunion'),
#             'equifax': request.POST.get('equifax'),
#             'judgments': request.POST.get('judgments') == 'yes',
#             'bankruptcy': request.POST.get('bankruptcy') == 'yes',
#             'personal_income': request.POST.get('personal_income'),
#         }

#         # Validate that required fields are not empty
#         if not business_data['business_legal_name']:
#             messages.error(request, "Business legal name is required.")
#             return redirect('business_registration')

#         # Create and save the Business object
#         try:
#             Business.objects.create(**business_data)
#             messages.success(request, "Business registration successful.")
#             return redirect('clientindex')
#         except IntegrityError as e:
#             messages.error(request, "There was an integrity error saving the business details.")
#             return redirect('business_registration')
#         except Exception as e:
#             messages.error(request, "There was an unexpected error saving the business details.")
#             return redirect('business_registration')

#     # Render the form with choice options
#     return render(request, 'clients/buisnessregistration.html', {
#         "state_choices": STATE_CHOICES,
#         "title_choices": TITLE_CHOICES,
#         "entity_choices": ENTITY_CHOICES,
#         "credit_choices": CREDIT_CHOICES,
#         "income_choices": PERSONAL_INCOME_CHOICES,
#         "month_choices": MONTH_CHOICES,
#         "year_choices": YEAR_CHOICES,
#         "industry_choices": INDUSTRY_CHOICES,
#         "amount_choices": AMOUNT_CHOICES,
#     })

