# client/views.py
import json,os
import logging


from django.conf import settings
from django.shortcuts import render, redirect,get_object_or_404

from serviceprovider.models import CustomUser  # Import your CustomUser model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import AccountInfo, OtherInfo, CustomerProfile
from serviceprovider.models import ServiceProviderProfile
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from serviceprovider.views import is_service_provider
from buisness.models import Business
from buisness.choices import (
    STATE_CHOICES, TITLE_CHOICES, ENTITY_CHOICES, CREDIT_CHOICES, 
    PERSONAL_INCOME_CHOICES, MONTH_CHOICES, YEAR_CHOICES, INDUSTRY_CHOICES, 
    AMOUNT_CHOICES,PRICE_LISTS
)

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        user_type = request.POST.get('user_type')

        if password != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('signup')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('signup')

        user = CustomUser.objects.create_user(username=username, email=email, password=password, user_type=user_type)
        user.save()

        if user_type == 'client':
            account_info = AccountInfo.objects.create(user=user, signup_date=timezone.now(), last_login=timezone.now())
            other_info = OtherInfo.objects.create(account=account_info)
            CustomerProfile.objects.create(user=user, account_info=account_info, other_info=other_info)
        elif user_type == 'service_provider':
            ServiceProviderProfile.objects.create(user=user)

        messages.success(request, "Account created successfully. Please log in.")
        return redirect('login')

    return render(request, 'clients/signup.html')
def login_view(request):
    logger = logging.getLogger(__name__)
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.get(email=email)  
            logger.info(f"User found with email: {user.username}")# Use CustomUser instead of User
        except CustomUser.DoesNotExist:
            messages.error(request, "Invalid email or password.")
            return redirect('login')

        # Authenticate using the username associated with the email
        user = authenticate(request, username=user.username, password=password)

        if user is not None:
            if user.is_active:  # Check if the user is active
                login(request, user)
                if user.user_type == 'client':
                    return redirect('clientindex')  # Redirect to client dashboard
                elif user.user_type == 'service_provider':
                    return redirect('index')  # Redirect to service provider dashboard
                else:
                    messages.error(request, "Unknown user type.")
                    return redirect('login')
            else:
                messages.error(request, "Account is inactive.")
                return redirect('login')
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login')
    return render(request, 'clients/login.html')
def logout_view(request):
    logout(request)  # This will log out the user
    return redirect('login') 


def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Check if new password and confirm password match
        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('reset_password')

        try:
            user = CustomUser.objects.get(email=email)
            # Update the user's password
            user.set_password(new_password)
            user.save()

            # Log out the user and clear the session to ensure they will log in with the new password
            logout(request)
            request.session.clear()  # Clear the session explicitly to remove any cached login state

            messages.success(request, "Password has been reset successfully. You can now log in with the new password.")
            return redirect('login')
        except CustomUser.DoesNotExist:
            messages.error(request, "No user found with that email address.")
            return redirect('reset_password')

    return render(request, 'clients/forgotpassword.html')


def is_client(user):
    return hasattr(user, 'customer_profile') and user.customer_profile is not None
@user_passes_test(is_client or is_service_provider, login_url='/login')
@login_required
def clientindex(request):
    user = request.user
    account_info = AccountInfo.objects.get(user=user)
    
    # Get the business associated with the user, if it exists
    business = Business.objects.filter(user=user).first()
    
    
    show_registration = business is None
    
    return render(request, 'clients/index.html', {
        'show_registration': show_registration,
        'state_choices':STATE_CHOICES,
        'year_choices':YEAR_CHOICES,
        'month_choices':MONTH_CHOICES,
        'industry_choices':INDUSTRY_CHOICES,
        'entity_choices':ENTITY_CHOICES,
        'amount_choices':AMOUNT_CHOICES,
        'credit_choices':CREDIT_CHOICES,
        'income_choices':PERSONAL_INCOME_CHOICES,
        
        'entity_compliant': business.entity_compliant() if business else False,
        'location_compliant': business.location_compliant() if business else False,
        'phones_compliant': business.phone_compilant() if business else False,
        'site_compliant': business.website_compilant() if business else False,
        'ein_compliant': business.ein_compliant() if business else False,
        'banking_compliant': business.banking_compilant() if business else False,
        'agencies_compliant': business.agencies_compilance() if business else False,
        'is_email_free': business.is_business_email_free() if business else True,
        'has_business_plan': business.has_business_plan() if business else False,
        'asset_compliance': business.asset_compliance() if business else False,
        'has_corp_only_facts':business.corp_compliance() if business else False,
        'business': business,
        
    })
@user_passes_test(is_client)
@login_required
def CompleteCompilance(request):
    user = request.user
    account_info = AccountInfo.objects.get(user=user)
    
    # Get the business associated with the user, if it exists
    business = Business.objects.filter(user=user).first()
    
    
    show_registration = business is None
    
    return render(request, 'clients/LenderCompilance/CompleteCompilance/CompleteCompliance.html', {
        'show_registration': show_registration,
        'state_choices':STATE_CHOICES,
        'year_choices':YEAR_CHOICES,
        'month_choices':MONTH_CHOICES,
        'industry_choices':INDUSTRY_CHOICES,
        'entity_choices':ENTITY_CHOICES,
        'amount_choices':AMOUNT_CHOICES,
        'credit_choices':CREDIT_CHOICES,
        'income_choices':PERSONAL_INCOME_CHOICES,
        
        'entity_compliant': business.entity_compliant() if business else False,
        'location_compliant': business.location_compliant() if business else False,
        'phones_compliant': business.phone_compilant() if business else False,
        'site_compliant': business.website_compilant() if business else False,
        'ein_compliant': business.ein_compliant() if business else False,
        'banking_compliant': business.banking_compilant() if business else False,
        'agencies_compliant': business.agencies_compilance() if business else False,
        'is_email_free': business.is_business_email_free() if business else True,
        'has_business_plan': business.has_business_plan() if business else False,
        'asset_compliance': business.asset_compliance() if business else False,
        'has_corp_only_facts':business.corp_compliance() if business else False,
        'business': business,
    })
@user_passes_test(is_client)
@login_required
def entityandfilings(request, pk):
    # Get the business instance for the logged-in user by primary key (pk)
    business = get_object_or_404(Business, pk=pk, user=request.user)

    # Handle form submission
    if request.method == "POST":
        entity_type = request.POST.get("entityType")
        state = request.POST.get("state")
        trademark_verified = request.POST.get("trademark") == "Yes"
        good_standing = request.POST.get("goodStanding") == "Yes"


        # Update the business model with the user inputs
        business.update_entity_info(entity_type, state, trademark_verified, good_standing)
        business.refresh_from_db()
        return redirect("business",business.pk)  
    
    return render(request, "clients/LenderCompilance/CompleteCompilance/Entity &Filings.html", {
        "business": business,
        
        'entity_compliant': business.entity_compliant() if business else False,
        'location_compliant': business.location_compliant() if business else False,
        'phones_compliant': business.phone_compilant() if business else False,
        'site_compliant': business.website_compilant() if business else False,
        'ein_compliant': business.ein_compliant() if business else False,
        'banking_compliant': business.banking_compilant() if business else False,
        'agencies_compliant': business.agencies_compilance() if business else False,
        'is_email_free': business.is_business_email_free() if business else True,
        'has_business_plan': business.has_business_plan() if business else False,
        'asset_compliance': business.asset_compliance() if business else False,
        'has_corp_only_facts':business.corp_compliance() if business else False,
        "state_choices": STATE_CHOICES,
        "buisness_types": ENTITY_CHOICES,
        
    })
@user_passes_test(is_client)
@login_required
def buisnesslocation(request, pk):
    # Get the business instance for the logged-in user by primary key (pk)
    business = get_object_or_404(Business, pk=pk, user=request.user)
    business_name = request.POST.get("businessName")
    primary_contact_first = request.POST.get("firstName")
    primary_contact_last = request.POST.get("lastName")
    contact_title = request.POST.get("contactTitle")
    contact_phone = request.POST.get("contactPhone")
    business_address = request.POST.get("businessAddress")
    city = request.POST.get("city")
    state = request.POST.get("state")
    zip_code = request.POST.get("zipCode")

    # Update the business instance with the new data
    business.update_location_info(business_name, primary_contact_first, primary_contact_last, contact_title, contact_phone, business_address, city, state, zip_code)

    
    if request.method == "POST":
        
        return redirect("phones",business.pk)  # Redirect to the dashboard or any other page

    return render(request, 'clients/LenderCompilance/CompleteCompilance/BuisnessLocation.html', {
        'business': business,
        'entity_compliant': business.entity_compliant() if business else False,
        'location_compliant': business.location_compliant() if business else False,
        'phones_compliant': business.phone_compilant() if business else False,
        'site_compliant': business.website_compilant() if business else False,
        'ein_compliant': business.ein_compliant() if business else False,
        'banking_compliant': business.banking_compilant() if business else False,
        'agencies_compliant': business.agencies_compilance() if business else False,
        'is_email_free': business.is_business_email_free() if business else True,
        'has_business_plan': business.has_business_plan() if business else False,
        'asset_compliance': business.asset_compliance() if business else False,
        'has_corp_only_facts':business.corp_compliance() if business else False,
        'title_choices':TITLE_CHOICES,
        'state_choices':STATE_CHOICES,
        
    })
@user_passes_test(is_client) 
@login_required
def phones(request,pk):
    # Get the business instance for the logged-in user by primary key (pk)
    business = get_object_or_404(Business, pk=pk, user=request.user)
    
    
    if request.method == "POST":
        # Get data from the form
        # Get data from the form
        listed_in_411 = request.POST.get("listed_in_411")=='true'
        phone_411 = request.POST.get("directory_phone_411")
        phone_800 = request.POST.get("directory_phone_800")
        submit_to_411= request.POST.get("submit_info_directory")=='true'
        fax_number = request.POST.get("fax_number")

        # Update the business instance with the new data
        business.update_phone_info(listed_in_411 , phone_411, submit_to_411, fax_number,phone_800 )
        return redirect("website",business.pk)  # Redirect to the dashboard or any other page


    return render(request, 'clients/LenderCompilance/CompleteCompilance/Phones&411.html', {
        'business': business,
        'entity_compliant': business.entity_compliant() if business else False,
        'location_compliant': business.location_compliant() if business else False,
        'phones_compliant': business.phone_compilant() if business else False,
        'site_compliant': business.website_compilant() if business else False,
        'ein_compliant': business.ein_compliant() if business else False,
        'banking_compliant': business.banking_compilant() if business else False,
        'agencies_compliant': business.agencies_compilance() if business else False,
        'is_email_free': business.is_business_email_free() if business else True,
        'has_business_plan': business.has_business_plan() if business else False,
        'asset_compliance': business.asset_compliance() if business else False,
        'has_corp_only_facts':business.corp_compliance() if business else False,
        "state_choices": STATE_CHOICES,
        "title_choices": TITLE_CHOICES,
        'is_email_free': business.is_business_email_free() if business else True
    })
    
@user_passes_test(is_client or is_service_provider)    
@login_required
def websites(request,pk):
    # Get the business instance for the logged-in user by primary key (pk)
    business = get_object_or_404(Business, pk=pk, user=request.user)
    
    
    if request.method == "POST":
        # Get data from the form
        # Get data from the form
        domain_name = request.POST.get("domain")
        business_mail= request.POST.get("buisness_mail")
        personal_mail = request.POST.get("personal_mail")
        
        # Update the business instance with the new data
        business.update_website_info(domain_name, business_mail, personal_mail )
        return redirect("ein",business.pk)  # Redirect to the dashboard or any other page


    return render(request, 'clients/LenderCompilance/CompleteCompilance/website&mail.html', {
        'business': business,
        
        'entity_compliant': business.entity_compliant() if business else False,
        'location_compliant': business.location_compliant() if business else False,
        'phones_compliant': business.phone_compilant() if business else False,
        'site_compliant': business.website_compilant() if business else False,
        'ein_compliant': business.ein_compliant() if business else False,
        'banking_compliant': business.banking_compilant() if business else False,
        'agencies_compliant': business.agencies_compilance() if business else False,
        'is_email_free': business.is_business_email_free() if business else True,
        'has_business_plan': business.has_business_plan() if business else False,
        'asset_compliance': business.asset_compliance() if business else False,
        'has_corp_only_facts':business.corp_compliance() if business else False,
    })
@user_passes_test(is_client or is_service_provider)    
@login_required   
def ein(request,pk):
    # Get the business instance for the logged-in user by primary key (pk)
    business = get_object_or_404(Business, pk=pk, user=request.user)
    
    
    if request.method == "POST":
        ein_verified = request.POST.get("ein_verified") == 'yes'
        licenses_obtained = request.POST.get("licenses_obtained") == 'yes'

        # Update the business instance with the new data
        business.update_ein_info(ein_verified, licenses_obtained)
        return redirect("banking", business.pk)
    
    return render(request, 'clients/LenderCompilance/CompleteCompilance/ein&icence.html', {
        'business': business,
        
        'entity_compliant': business.entity_compliant() if business else False,
        'location_compliant': business.location_compliant() if business else False,
        'phones_compliant': business.phone_compilant() if business else False,
        'site_compliant': business.website_compilant() if business else False,
        'ein_compliant': business.ein_compliant() if business else False,
        'banking_compliant': business.banking_compilant() if business else False,
        'agencies_compliant': business.agencies_compilance() if business else False,
        'is_email_free': business.is_business_email_free() if business else True,
        'has_business_plan': business.has_business_plan() if business else False,
        'asset_compliance': business.asset_compliance() if business else False,
        'has_corp_only_facts':business.corp_compliance() if business else False,

    })
    
@user_passes_test(is_client or is_service_provider)    
@login_required   
def banking(request,pk):
    business = get_object_or_404(Business, pk=pk, user=request.user)
    if request.method == "POST":
        account_linked = request.POST.get("account_linked") == 'yes'
        establish_merchant_account = request.POST.get("establish_merchant_account") == 'yes'

        # Update the business instance with the new data
        business.update_banking_info(account_linked, establish_merchant_account)
        return redirect("agencies",business.pk)  # Redirect to the dashboard or any other page


    return render(request, 'clients/LenderCompilance/CompleteCompilance/buisnessbanking.html', {
        'business': business,
        'entity_compliant': business.entity_compliant() if business else False,
        'location_compliant': business.location_compliant() if business else False,
        'phones_compliant': business.phone_compilant() if business else False,
        'site_compliant': business.website_compilant() if business else False,
        'ein_compliant': business.ein_compliant() if business else False,
        'banking_compliant': business.banking_compilant() if business else False,
        'agencies_compliant': business.agencies_compilance() if business else False,
        'is_email_free': business.is_business_email_free() if business else True,
        'has_business_plan': business.has_business_plan() if business else False,
        'asset_compliance': business.asset_compliance() if business else False,
        'has_corp_only_facts':business.corp_compliance() if business else False,

    })
@user_passes_test(is_client or is_service_provider)
@login_required    
def sos_contact_list(request,pk):
    json_file_path=json_file_path = os.path.join(
        settings.BASE_DIR, "clients", "static", "json_files", "state_list.json"
    )
    with open(json_file_path,'r') as file:
        sos_data=json.load(file)
    business = get_object_or_404(Business, pk=pk, user=request.user)
    return render(request, 'clients/LenderCompilance/CompleteCompilance/sos_contact.html', {
        'business': business,
        'sos_data':sos_data,
        
        'entity_compliant': business.entity_compliant() if business else False,
        'location_compliant': business.location_compliant() if business else False,
        'phones_compliant': business.phone_compilant() if business else False,
        'site_compliant': business.website_compilant() if business else False,
        'ein_compliant': business.ein_compliant() if business else False,
        'banking_compliant': business.banking_compilant() if business else False,
        'agencies_compliant': business.agencies_compilance() if business else False,
        'is_email_free': business.is_business_email_free() if business else True,
        'has_business_plan': business.has_business_plan() if business else False,
        'asset_compliance': business.asset_compliance() if business else False,
        'has_corp_only_facts':business.corp_compliance() if business else False,

    })   
@user_passes_test(is_client or is_service_provider)
@login_required
def agencies(request,pk):
    business = get_object_or_404(Business, pk=pk, user=request.user)
    if request.method == "POST":
        print("Received POST data from agency page:", request.POST)
        # Get data from the form
        business_filing_status = request.POST.get("business_filing_status") == 'yes'
        country_licence_permit = request.POST.get("country_licence_permit") == 'yes'
        city_licence_permit = request.POST.get("city_licence_permit") == 'yes'
        irs_filings = request.POST.get("irs_filings") == 'yes'
        account_status = request.POST.get("account_status") == 'yes'
        directory_assistance = request.POST.get("directory_assistance") == 'yes'
        
        # Update the business instance with the new data
        business.update_agencies_info(
            business_filing_status,
            country_licence_permit,
            city_licence_permit,
            irs_filings,
            account_status,
            directory_assistance
        )
        return redirect("clientindex")  # Redirect to the dashboard or any other page


    return render(request, 'clients/LenderCompilance/CompleteCompilance/Agencies&NAICS.html', {
        'business': business,
        'entity_compliant': business.entity_compliant() if business else False,
        'location_compliant': business.location_compliant() if business else False,
        'phones_compliant': business.phone_compilant() if business else False,
        'site_compliant':business.website_compilant() if business else False,
        'ein_compliant':business.ein_compliant() if business else False,
        'banking_compliant':business.banking_compilant() if business else False,
        'agencies_compliant':business.agencies_compilance() if business else False,
        'is_email_free': business.is_business_email_free() if business else True

    })
    

@user_passes_test(is_client)
@login_required
def businessplan(request, pk):
    # Get the business instance for the logged-in user by primary key (pk)
    business = get_object_or_404(Business, pk=pk, user=request.user)

    # Handle form submission
    if request.method == "POST":
        print("Received POST data from agency page:", request.POST)
        # Fetch value from form submission
        business_plan = request.POST.get("business_plan") == "Yes"
        # Update and save business plan status
        business.update_business_plan(business_plan)
        business.refresh_from_db()
        return redirect("business_assets",business.pk)  
    
    return render(request, "clients/LenderCompilance/GettingApproved/Businessplan.html", {
        "business": business,
        
        'entity_compliant': business.entity_compliant() if business else False,
        'location_compliant': business.location_compliant() if business else False,
        'phones_compliant': business.phone_compilant() if business else False,
        'site_compliant': business.website_compilant() if business else False,
        'ein_compliant': business.ein_compliant() if business else False,
        'banking_compliant': business.banking_compilant() if business else False,
        'agencies_compliant': business.agencies_compilance() if business else False,
        'is_email_free': business.is_business_email_free() if business else True,
        'has_business_plan': business.has_business_plan() if business else False,
        'asset_compliance': business.asset_compliance() if business else False,
        'has_corp_only_facts':business.corp_compliance() if business else False,
        
    })
    

@user_passes_test(is_client) 
@login_required
def business_assets(request, pk):
    # Get the business instance for the logged-in user by primary key (pk)
    business = get_object_or_404(Business, pk=pk, user=request.user)

    # Handle form submission
    if request.method == "POST":
        # Fetch values from form submission
        own_residential_real_estate = request.POST.get("own_residential_real_estate") == 'Yes'
        market_value_real_estate = request.POST.get("market_value_real_estate") 
        owed_against_real_estate = request.POST.get("owed_against_real_estate") 
        real_estate_secured_note_payment = request.POST.get("real_estate_secured_note_payment") 
        structured_settlement_payment = request.POST.get("structured_settlement_payment") 
        ira_401k_value = request.POST.get("ira_401k_value") 
        outstanding_invoices = request.POST.get("outstanding_invoices") 
        existing_purchase_orders = request.POST.get("existing_purchase_orders") 
        equipment_owned_value = request.POST.get("equipment_owned_value") 
        
        # Update the business instance with new asset data
        business.update_assets(
            own_residential_real_estate,
            market_value_real_estate,
            owed_against_real_estate,
            real_estate_secured_note_payment,
            structured_settlement_payment,
            ira_401k_value,
            outstanding_invoices,
            existing_purchase_orders,
            equipment_owned_value
        )
        
        

        # Redirect to business page after saving
        return redirect("corponlyfacts", business.pk)  

    # Render the form with the current business data
    return render(request, "clients/LenderCompilance/GettingApproved/BuisnessAssets.html", {
        "business": business,
        "price_choices": PRICE_LISTS,  # Assuming you have a constant PRICE_LISTS or equivalent
        'entity_compliant': business.entity_compliant() if business else False,
        'location_compliant': business.location_compliant() if business else False,
        'phones_compliant': business.phone_compilant() if business else False,
        'site_compliant': business.website_compilant() if business else False,
        'ein_compliant': business.ein_compliant() if business else False,
        'banking_compliant': business.banking_compilant() if business else False,
        'agencies_compliant': business.agencies_compilance() if business else False,
        'is_email_free': business.is_business_email_free() if business else True,
        'has_business_plan': business.has_business_plan() if business else False,
        'asset_compliance': business.asset_compliance() if business else False,
        'has_corp_only_facts': business.corp_compliance() if business else False,
    })




# Assuming `is_client` is a custom decorator that checks if the user is a client
@user_passes_test(is_client) 
@login_required
def corponlyfacts(request, pk):
    # Get the business instance for the logged-in user by primary key (pk)
    business = get_object_or_404(Business, pk=pk, user=request.user)

    # Handle form submission
    if request.method == "POST":
        print("Received POST data from agency page:", request.POST)

        # Fetch values from form submission
        experian_score = request.POST.get("experian")
        transunion_score = request.POST.get("transUnion")
        equifax_score = request.POST.get("equifax")

        business.update_corp_only_facts(experian_score,transunion_score,equifax_score)
        # Optionally, you can call refresh_from_db() to reload the object from the database
        business.refresh_from_db()

        # Redirect to the business page after successful submission
        return redirect("bankrating", business.pk)  

    # Render the page with the current business data
    return render(request, "clients/LenderCompilance/GettingApproved/CorpOnlyFacts.html", {
        "business": business,
        'entity_compliant': business.entity_compliant() if business else False,
        'location_compliant': business.location_compliant() if business else False,
        'phones_compliant': business.phone_compilant() if business else False,
        'site_compliant': business.website_compilant() if business else False,
        'ein_compliant': business.ein_compliant() if business else False,
        'banking_compliant': business.banking_compilant() if business else False,
        'agencies_compliant': business.agencies_compilance() if business else False,
        'is_email_free': business.is_business_email_free() if business else True,
        'has_business_plan': business.has_business_plan() if business else False,
        'asset_compliance': business.asset_compliance() if business else False,
        'has_corp_only_facts':business.corp_compliance() if business else False,
    })
# Assuming `is_client` is a custom decorator that checks if the user is a client
@user_passes_test(is_client) 
@login_required
def Bank_rating(request, pk):
    # Get the business instance for the logged-in user by primary key (pk)
    business = get_object_or_404(Business, pk=pk, user=request.user)

    # Handle form submission
    if request.method == "POST":
        print("Received POST data from agency page:", request.POST)

        # Fetch values from form submission
        last_balance = request.POST.get("last_balance")
        
        business.update_bankrating(last_balance)
        # Optionally, you can call refresh_from_db() to reload the object from the database
        business.refresh_from_db()

        # Redirect to the business page after successful submission
        return redirect("comparablecredit", business.pk)  

    # Render the page with the current business data
    return render(request, "clients/LenderCompilance/GettingApproved/YourBankRating.html", {
        "business": business,
        'price_choices': PRICE_LISTS,
        'entity_compliant': business.entity_compliant() if business else False,
        'location_compliant': business.location_compliant() if business else False,
        'phones_compliant': business.phone_compilant() if business else False,
        'site_compliant': business.website_compilant() if business else False,
        'ein_compliant': business.ein_compliant() if business else False,
        'banking_compliant': business.banking_compilant() if business else False,
        'agencies_compliant': business.agencies_compilance() if business else False,
        'is_email_free': business.is_business_email_free() if business else True,
        'has_business_plan': business.has_business_plan() if business else False,
        'asset_compliance': business.asset_compliance() if business else False,
        'has_corp_only_facts':business.corp_compliance() if business else False,
    })

@user_passes_test(is_client) 
@login_required
def Comparable_credit(request, pk):
    # Get the business instance for the logged-in user by primary key (pk)
    business = get_object_or_404(Business, pk=pk, user=request.user)

    # Handle form submission
    if request.method == "POST":
        print("Received POST data from agency page:", request.POST)

        # Fetch the 'cd_loan_status' value from the form submission
        secured_loan_status = request.POST.get("secured_loan_status")

        # Update the business instance with the new cd_loan_status value
        if secured_loan_status:
            business.secured_loan_status = secured_loan_status
        
        # Save the updated business instance
        business.save()
        business.refresh_from_db()    
        # Redirect to the business page after successful submission
        return redirect("businessloan", business.pk)  

    # Render the page with the current business data
    return render(request, "clients/LenderCompilance/GettingApproved/ComparableCredits.html", {
        "business": business,
        'price_choices': PRICE_LISTS,
        'entity_compliant': business.entity_compliant() if business else False,
        'location_compliant': business.location_compliant() if business else False,
        'phones_compliant': business.phone_compilant() if business else False,
        'site_compliant': business.website_compilant() if business else False,
        'ein_compliant': business.ein_compliant() if business else False,
        'banking_compliant': business.banking_compilant() if business else False,
        'agencies_compliant': business.agencies_compilance() if business else False,
        'is_email_free': business.is_business_email_free() if business else True,
        'has_business_plan': business.has_business_plan() if business else False,
        'asset_compliance': business.asset_compliance() if business else False,
        'has_corp_only_facts':business.corp_compliance() if business else False,
    })
@user_passes_test(is_client) 
@login_required
def Cd_loan(request, pk):
    # Get the business instance for the logged-in user by primary key (pk)
    business = get_object_or_404(Business, pk=pk, user=request.user)

    # Handle form submission
    if request.method == "POST":
        print("Received POST data from agency page:", request.POST)

        
        # Fetch the 'cd_loan_status' value from the form submission
        cd_loan_status = request.POST.get("cd_loan_status")

        # Update the business instance with the new cd_loan_status value
        if cd_loan_status:
            business.cd_loan_status = cd_loan_status
        
        # Save the updated business instance
        business.save()
        business.refresh_from_db() 
        # Redirect to the business page after successful submission
        return redirect("clientindex")  

    # Render the page with the current business data
    return render(request, "clients/LenderCompilance/GettingApproved/CDBusinessLoan.html", {
        "business": business,
        'price_choices': PRICE_LISTS,
        'entity_compliant': business.entity_compliant() if business else False,
        'location_compliant': business.location_compliant() if business else False,
        'phones_compliant': business.phone_compilant() if business else False,
        'site_compliant': business.website_compilant() if business else False,
        'ein_compliant': business.ein_compliant() if business else False,
        'banking_compliant': business.banking_compilant() if business else False,
        'agencies_compliant': business.agencies_compilance() if business else False,
        'is_email_free': business.is_business_email_free() if business else True,
        'has_business_plan': business.has_business_plan() if business else False,
        'asset_compliance': business.asset_compliance() if business else False,
        'has_corp_only_facts':business.corp_compliance() if business else False,
    })