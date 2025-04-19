from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth import get_backends
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.db import transaction
from buisness.models import Business
from .utils import is_client, is_service_provider
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from serviceprovider.models import CustomUser,ServiceProviderProfile
# from clients.models import AccountInfo,OtherInfo,CustomerProfile 
from django.db import transaction
from django.http import Http404

@user_passes_test(is_service_provider)
@login_required
def index(request):
    # Fetch users (CustomUser) and their related businesses through Client model
    users = CustomUser.objects.filter(user_type='client').prefetch_related('client_profile__businesses', 'account_info').all()

    # Add pagination
    paginator = Paginator(users, 10)  # Show 10 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'serviceprovider/index.html', {'page_obj': page_obj})
@user_passes_test(is_service_provider)
@login_required
def membersearch(request):
    users = CustomUser.objects.filter(user_type='client').prefetch_related('client_profile__businesses', 'account_info').all()  # Fetch all users with related data

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
            filters &= Q(client_profile__businesses__business_legal_name__icontains=company)
        if email:
            filters &= Q(email__icontains=email)
        if phone:
            filters &= Q(client_profile__businesses__phone__icontains=phone)
        if first_name:
            filters &= Q(client_profile__businesses__first_name__icontains=first_name)
        if last_name:
            filters &= Q(client_profile__businesses__last_name__icontains=last_name)
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
    users = CustomUser.objects.filter(user_type='client').prefetch_related(
        'client_profile__businesses',  # Prefetch businesses related to client_profile
        'account_info',  # Prefetch account_info
        'customer_profile__other_info'  # Prefetch other_info related to customer_profile
    ).all()
    
    # Add pagination
    paginator = Paginator(users, 10)  # Show 10 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Render the template
    return render(request, 'serviceprovider/tables.html', {'page_obj': page_obj})
@user_passes_test(is_service_provider)
@login_required
def editmembers(request, user_id):
    # Fetch user with related client profile and businesses in a single query
    user = get_object_or_404(
        CustomUser.objects.filter(user_type='client')
        .select_related('client_profile')  # Fetch client_profile in a single query
        .prefetch_related('client_profile__businesses'),  # Fetch businesses for the client in one query
        pk=user_id
    )

    # Extract client profile and business (if available)
    client_profile = user.client_profile
    business = client_profile.businesses.first() if client_profile else None

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
        if client_profile:
            client_profile.first_name = first_name
            client_profile.last_name = last_name
            client_profile.save()
        user.save()

        # Update business fields
        if business:
            business.business_legal_name = company
            business.address = address
            business.state = state
            business.zip_code = zip_code
            business.domain_name = domain
            business.save()

    return render(request, 'serviceprovider/edit.html', {'user': user, 'business': business, 'client_profile': client_profile})

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
                Business.objects.filter(client=user.client_profile).delete()

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
from serviceprovider.models import CustomUser  # Make sure to import your custom user model

@user_passes_test(lambda u: is_client(u) or is_service_provider(u), login_url='/login')
def loginasuser(request, user_id):
    if request.user.is_superuser or is_service_provider(request.user):  # Ensure the user is a service provider
        # Retrieve the user to log in as
        user = get_object_or_404(CustomUser, pk=user_id)  # Use CustomUser instead of User
        
        # Log in as the specified user
        login(request, user)
        
        # Redirect to the user-specific page, such as a client dashboard or index
        return HttpResponseRedirect(reverse('clientindex', args=[user.id]))

    
    return redirect('service_provider')  # Redirect to service provider page if not authorized
# @user_passes_test(is_service_provider)
# @login_required
# def membersearch(request):
#     users = CustomUser.objects.filter(user_type='client').prefetch_related('businesses', 'account_info').all() # Fetch all users with related data

#     if request.method == 'GET':
#         # Fetch input values from request.GET
#         company = request.GET.get('company', '').strip()
#         email = request.GET.get('email', '').strip()
#         phone = request.GET.get('phone', '').strip()
#         first_name = request.GET.get('firstname', '').strip()
#         last_name = request.GET.get('lastname', '').strip()
#         user_id = request.GET.get('user_id', '').strip()
#         lastlogin_from = request.GET.get('lastlogin_from', '').strip()
#         lastlogin_to = request.GET.get('lastlogin_to', '').strip()
#         paid_user = request.GET.get('paid_user', 'All').strip()
#         applied = request.GET.get('applied', 'All').strip()
#         integrated_reports = request.GET.get('integrated_reports', 'All').strip()

#         # Initialize the filter condition using Q objects
#         filters = Q()

#         # Add dynamic filtering
#         if company:
#             filters &= Q(businesses__business_legal_name__icontains=company)
#         if email:
#             filters &= Q(email__icontains=email)
#         if phone:
#             filters &= Q(businesses__phone__icontains=phone)
#         if first_name:
#             filters &= Q(businesses__first_name__icontains=first_name)
#         if last_name:
#             filters &= Q(businesses__last_name__icontains=last_name)
#         if user_id:
#             filters &= Q(id=user_id)
#         if lastlogin_from:
#             filters &= Q(account_info__last_login__gte=lastlogin_from)
#         if lastlogin_to:
#             filters &= Q(account_info__last_login__lte=lastlogin_to)
#         if paid_user != 'All':
#             filters &= Q(customer_profile__paid_user=(paid_user == 'Yes'))
#         if applied != 'All':
#             filters &= Q(customer_profile__applied=(applied == 'Yes'))
#         if integrated_reports != 'All':
#             filters &= Q(customer_profile__integrated_reports=(integrated_reports == 'Yes'))

#         # Apply filters if any filter condition exists
#         if filters:
#             users = users.filter(filters).distinct()

#     # Add pagination
#     paginator = Paginator(users, 10)  # Show 10 users per page
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     # Render the template
#     return render(request, 'serviceprovider/searchmembers.html', {'page_obj': page_obj})

# @user_passes_test(is_service_provider)
# @login_required
# def viewmembers(request):
#     # Fetch users with related businesses and account info
#     users = CustomUser.objects.filter(user_type='client').prefetch_related('businesses', 'account_info').all()

#     # Add pagination
#     paginator = Paginator(users, 10)  # Show 10 users per page
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     # Render the template
#     return render(request, 'serviceprovider/tables.html', {'page_obj': page_obj})

# @user_passes_test(is_service_provider)
# @login_required
#  # Ensure that all database updates are done atomically
# def editmembers(request, user_id):
#     # Fetch user and related business data
#     user = get_object_or_404(
#         CustomUser.objects.filter(user_type='client').prefetch_related('businesses', 'account_info'),
#         pk=user_id
#     )
#     business = user.businesses.first()  # Fetch the user's business (assuming one business per user)

#     if request.method == 'POST':
#         # Fetch input values from request.POST
#         company = request.POST.get('company')
#         address = request.POST.get('address')
#         first_name = request.POST.get('firstname')
#         last_name = request.POST.get('lastname')
#         state = request.POST.get('state')
#         zip_code = request.POST.get('zip_code')
#         domain = request.POST.get('business_domain')
#         user_name = request.POST.get('user_name')
#         password = request.POST.get('password')

#         # Update user fields
#         user.username = user_name
#         if password:  # Only update if a password is provided
#             user.set_password(password)
#         user.first_name = first_name
#         user.last_name = last_name
#         user.save()

#         # Update business fields
#         if business:
#             business.business_legal_name = company
#             business.address = address
#             business.state = state
#             business.zip_code = zip_code
#             business.domain_name = domain
#             business.save()

#     return render(request, 'serviceprovider/edit.html', {'user': user, 'business': business})



# # Make sure the user is a service provider
# @user_passes_test(is_service_provider)
# @login_required
# def deletemember(request, user_id):
#     # Ensure that the user being deleted exists
#     user = get_object_or_404(CustomUser, pk=user_id)

#     if request.method == 'POST':  # Ensure deletion happens only on POST request
#         try:
#             # Start a transaction to ensure atomicity
#             with transaction.atomic():
#                 # Deleting related models manually
#                 if hasattr(user, 'service_provider_profile'):
#                     user.service_provider_profile.delete()

#                 # Delete associated Business records
#                 Business.objects.filter(user=user).delete()

#                 # # Delete associated AccountInfo records
#                 # AccountInfo.objects.filter(user=user).delete()

#                 # # Delete associated CustomerProfile records
#                 # CustomerProfile.objects.filter(user=user).delete()

#                 # # Delete associated OtherInfo records (through AccountInfo)
#                 # OtherInfo.objects.filter(account__user=user).delete()

#                 # Finally, delete the User record itself
#                 user.delete()

#             # Show a success message
#             messages.success(request, "User and related data have been successfully deleted.")
#             return redirect('index')  # Redirect to your success page after deletion
#         except Exception as e:
#             # If any error occurs, show an error message
#             messages.error(request, f"An error occurred while deleting the user: {str(e)}")
#             return redirect('index')  # Redirect to your error page if deletion fails

#     # If the request method is not POST, just redirect back (error handling)
#     return redirect('index')  # Update with your error page URL
# @user_passes_test(is_service_provider, login_url='/login')
# @login_required
# def loginasuser(request, user_id):
#     user = get_object_or_404(
#         CustomUser.objects.filter(user_type='client').prefetch_related('businesses', 'account_info'),
#         pk=user_id
#     )

#     print(f"Before Impersonation: {request.user}")
#     request.session.flush()  # 🔥 Completely resets session before switching user

#     #  This line sets the auth backend manually
#     user.backend = get_backends()[0].__module__  
    
#     login(request, user)
#     request.session.save()

#     print(f"After Impersonation: {request.user}")
#     return HttpResponseRedirect(reverse('clientindex'))

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