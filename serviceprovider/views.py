from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth import login
from django.contrib import messages
from django.db import transaction
from buisness.models import Business
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from serviceprovider.models import CustomUser,ServiceProviderProfile
from clients.models import AccountInfo,OtherInfo,CustomerProfile 
from django.db import transaction
from django.http import Http404
def is_service_provider(user):
    return hasattr(user, 'service_provider_profile')
@user_passes_test(is_service_provider)

@login_required
def index(request):
    # Fetch users with related businesses and account info
    users = CustomUser.objects.filter(user_type='client').prefetch_related('businesses', 'account_info').all()

    # Add pagination
    paginator = Paginator(users, 10)  # Show 10 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

   

    return render(request,'serviceprovider/index.html',{'page_obj': page_obj})


@user_passes_test(is_service_provider)
@login_required
def membersearch(request):
    users = CustomUser.objects.filter(user_type='client').prefetch_related('businesses', 'account_info').all() # Fetch all users with related data

    if request.method == 'GET':
        # Fetch input values from request.GET
        company = request.GET.get('company', '').strip()
        email = request.GET.get('email', '').strip()
        phone = request.GET.get('phone', '').strip()
        first_name = request.GET.get('firstname', '').strip()
        last_name = request.GET.get('lastname', '').strip()
        user_id = request.GET.get('user_id', '').strip()
        lastlogin_from = request.GET.get('lastlogin_from', '').strip()
        lastlogin_to = request.GET.get('lastlogin_to', '').strip()
        paid_user = request.GET.get('paid_user', 'All').strip()
        applied = request.GET.get('applied', 'All').strip()
        integrated_reports = request.GET.get('integrated_reports', 'All').strip()

        # Initialize the filter condition using Q objects
        filters = Q()

        # Add dynamic filtering
        if company:
            filters &= Q(businesses__business_legal_name__icontains=company)
        if email:
            filters &= Q(email__icontains=email)
        if phone:
            filters &= Q(businesses__phone__icontains=phone)
        if first_name:
            filters &= Q(businesses__first_name__icontains=first_name)
        if last_name:
            filters &= Q(businesses__last_name__icontains=last_name)
        if user_id:
            filters &= Q(id=user_id)
        if lastlogin_from:
            filters &= Q(account_info__last_login__gte=lastlogin_from)
        if lastlogin_to:
            filters &= Q(account_info__last_login__lte=lastlogin_to)
        if paid_user != 'All':
            filters &= Q(customer_profile__paid_user=(paid_user == 'Yes'))
        if applied != 'All':
            filters &= Q(customer_profile__applied=(applied == 'Yes'))
        if integrated_reports != 'All':
            filters &= Q(customer_profile__integrated_reports=(integrated_reports == 'Yes'))

        # Apply filters if any filter condition exists
        if filters:
            users = users.filter(filters).distinct()

    # Add pagination
    paginator = Paginator(users, 10)  # Show 10 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Render the template
    return render(request, 'serviceprovider/searchmembers.html', {'page_obj': page_obj})

@user_passes_test(is_service_provider)
@login_required
def viewmembers(request):
    # Fetch users with related businesses and account info
    users = CustomUser.objects.filter(user_type='client').prefetch_related('businesses', 'account_info').all()

    # Add pagination
    paginator = Paginator(users, 10)  # Show 10 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Render the template
    return render(request, 'serviceprovider/tables.html', {'page_obj': page_obj})

@user_passes_test(is_service_provider)
@login_required
 # Ensure that all database updates are done atomically
def editmembers(request, user_id):
    # Fetch user and related business data
    user = get_object_or_404(
        CustomUser.objects.filter(user_type='client').prefetch_related('businesses', 'account_info'),
        pk=user_id
    )
    business = user.businesses.first()  # Fetch the user's business (assuming one business per user)

    if request.method == 'POST':
        # Fetch input values from request.POST
        company = request.POST.get('company')
        address = request.POST.get('address')
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        domain = request.POST.get('business_domain')
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')

        # Update user fields
        user.username = user_name
        if password:  # Only update if a password is provided
            user.set_password(password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # Update business fields
        if business:
            business.business_legal_name = company
            business.address = address
            business.state = state
            business.zip_code = zip_code
            business.domain_name = domain
            business.save()

    return render(request, 'serviceprovider/edit.html', {'user': user, 'business': business})



# Make sure the user is a service provider
@user_passes_test(is_service_provider)
@login_required
def deletemember(request, user_id):
    # Ensure that the user being deleted exists
    user = get_object_or_404(CustomUser, pk=user_id)

    if request.method == 'POST':  # Ensure deletion happens only on POST request
        try:
            # Start a transaction to ensure atomicity
            with transaction.atomic():
                # Deleting related models manually
                if hasattr(user, 'service_provider_profile'):
                    user.service_provider_profile.delete()

                # Delete associated Business records
                Business.objects.filter(user=user).delete()

                # Delete associated AccountInfo records
                AccountInfo.objects.filter(user=user).delete()

                # Delete associated CustomerProfile records
                CustomerProfile.objects.filter(user=user).delete()

                # Delete associated OtherInfo records (through AccountInfo)
                OtherInfo.objects.filter(account__user=user).delete()

                # Finally, delete the User record itself
                user.delete()

            # Show a success message
            messages.success(request, "User and related data have been successfully deleted.")
            return redirect('index')  # Redirect to your success page after deletion
        except Exception as e:
            # If any error occurs, show an error message
            messages.error(request, f"An error occurred while deleting the user: {str(e)}")
            return redirect('index')  # Redirect to your error page if deletion fails

    # If the request method is not POST, just redirect back (error handling)
    return redirect('index')  # Update with your error page URL
@user_passes_test(is_service_provider)
@login_required
def loginasuser(request, user_id):
    # Fetch the user to impersonate
    user = get_object_or_404(
        CustomUser.objects.filter(user_type='client').prefetch_related('businesses', 'account_info'),
        pk=user_id
    )
    
    # Set up the session for the impersonated user
    login(request, user)
    
    # Ensure the business is fetched and passed to the template
    business = Business.objects.filter(user=user).first()  # Assuming the user has a business
    
    return render(request, 'clients/index.html', {
        'user': user,
        'business': business,
        'entity_compliant': business.entity_compliant() if business else False,
        'location_compliant': business.location_compliant() if business else False,
        'phones_compliant': business.phone_compliant() if business else False,
        'site_compliant': business.website_compilant() if business else False,
        'ein_compliant': business.ein_compliant() if business else False,
        'banking_compliant': business.banking_compilant() if business else False,
        'agencies_compliant': business.agencies_compilance() if business else False,
    })


# @user_passes_test(lambda user: user.is_superuser)
# def loginasuser(request,user_id):
#     if request.user.is_superuser or is_service_provider:
#         # Retrieve the user to log in as
#         user = get_object_or_404(User, pk=user_id)
        
#         # Log in as the specified user
#         login(request, user)
        
#         # Redirect to the user-specific page, such as a client dashboard or index
#         return HttpResponseRedirect(reverse('client_index', args=[user.id]))  # Customize based on your needs
    
#     return redirect('service_provider')  