from django.db import models
from django.conf import settings
from buisness.models import Client as BusinessClient
from serviceprovider.models import CustomUser

class AccountInfo(models.Model): 
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="account_info")
    last_login = models.DateTimeField(null=True, blank=True) # Can be null on initial creation
    signup_date = models.DateTimeField(auto_now_add=True)
    allow_bonus_vendors_access = models.BooleanField(default=False)

    def __str__(self):
        return f"Account Info for {self.user.username}"
class OtherInfo(models.Model):
    account = models.OneToOneField(AccountInfo, on_delete=models.CASCADE, related_name='other_info')
    paid_user = models.BooleanField(default=False)
    status = models.CharField(max_length=50, choices=[('Active', 'Active'), ('Responding', 'Responding'), ('Inactive', 'Inactive')], default='Inactive') # Set a default

    def __str__(self):
        return f"Other Info for {self.account.username}"

class CustomerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="customer_profile")
    other_info = models.OneToOneField(OtherInfo, on_delete=models.CASCADE, related_name="customer_profile")

    def __str__(self):
        return f"Customer Profile of {self.user.username}"
# # client/models.py
# from django.contrib.auth.models import User
# from django.db import models
# from django.conf import settings
# from buisness.models import Client
# # class Client(models.Model):
# #     # You can add additional fields here for client-specific data
# #     first_name = models.CharField(max_length=50)
# #     last_name = models.CharField(max_length=50)
# #     email = models.EmailField(unique=True)

# #     def __str__(self):
# #         return f"{self.first_name} {self.last_name}"

# class AccountInfo(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="account_info")
#     last_login = models.DateTimeField()
#     signup_date = models.DateTimeField()
#     allow_bonus_vendors_access = models.BooleanField(default=False)

#     def __str__(self):
#         return f"Account Info for {self.user.username}"
# class OtherInfo(models.Model):
#     account = models.OneToOneField(AccountInfo, on_delete=models.CASCADE, related_name='other_info')
#     paid_user = models.BooleanField(default=False)
#     status = models.CharField(max_length=50, choices=[('Active', 'Active'), ('Responding', 'Responding'), ('Inactive', 'Inactive')])
#     def __str__(self):
#         return f"Other Info for {self.account.username}"

# class CustomerProfile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="customer_profile")
#     client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name='customer_profile')
#     account_info = models.OneToOneField(AccountInfo, on_delete=models.CASCADE, related_name="customer_profile")
#     other_info = models.OneToOneField(OtherInfo, on_delete=models.CASCADE, related_name="customer_profile")

#     def __str__(self):
#         return f"Customer Profile of {self.user.username}"



