# client/models.py
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
class AccountInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="account_info")
    last_login = models.DateTimeField()
    signup_date = models.DateTimeField()
    allow_bonus_vendors_access = models.BooleanField(default=False)

    def __str__(self):
        return f"Account Info for {self.user.username}"
class OtherInfo(models.Model):
    account = models.OneToOneField(AccountInfo, on_delete=models.CASCADE, related_name='other_info')
    paid_user = models.BooleanField(default=False)
    status = models.CharField(max_length=50, choices=[('Active', 'Active'), ('Responding', 'Responding'), ('Inactive', 'Inactive')])
    def __str__(self):
        return f"Other Info for {self.account.username}"

class CustomerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="customer_profile")
    account_info = models.OneToOneField(AccountInfo, on_delete=models.CASCADE, related_name="customer_profile")
    other_info = models.OneToOneField(OtherInfo, on_delete=models.CASCADE, related_name="customer_profile")

    def __str__(self):
        return f"Customer Profile of {self.user.username}"




# from django.db import models
# from django.core.validators import RegexValidator
# from django.contrib.auth.models import User
# class ContactInfo(models.Model):
#     PHONE_REGEX = RegexValidator(regex=r'^\+?1?\d{10}$', message="Phone number must be in the format: '+1234567890'. Up to 10 digits allowed.")

#     company = models.CharField(max_length=255)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     phone = models.CharField(validators=[PHONE_REGEX], max_length=10, verbose_name="Phone (Cell Phone)")
#     address = models.CharField(max_length=255)
#     city = models.CharField(max_length=100)
#     state = models.CharField(max_length=2, choices=[
#         ('AL', 'Alabama'), ('NY', 'New York'), ('CA', 'California'), # Add the rest of the U.S. states
#     ])
#     zip_code = models.CharField(max_length=5)
#     email = models.EmailField()

#     def __str__(self):
#         return f"{self.first_name} {self.last_name} - {self.company}"
# class AccountInfo(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer_profile")
#     username = models.CharField(max_length=50)
#     password = models.CharField(max_length=50)
#     last_login = models.DateTimeField()
#     site = models.URLField()
#     step = models.CharField(max_length=255, verbose_name="Current Step")
#     user_type = models.CharField(max_length=20, choices=[
#         ('User', 'User'),
#         ('Admin', 'Admin'),
#     ])
#     signup_date = models.DateTimeField()
#     allow_bonus_vendors_access = models.BooleanField(default=False)

#     def __str__(self):
#         return f"Account Info for {self.username}"
# class OtherInfo(models.Model):
#     account = models.OneToOneField(AccountInfo, on_delete=models.CASCADE, related_name='other_info')
#     paid_user = models.BooleanField(default=False)
#     paid_user_activated_date = models.DateField(null=True, blank=True)
#     payment_approved = models.BooleanField(default=False)
#     status = models.CharField(max_length=50, choices=[
#         ('Active', 'Active'),
#         ('Responding', 'Responding'),
#         ('Inactive', 'Inactive'),
#     ])
#     notes = models.TextField(null=True, blank=True)
#     timer_days = models.IntegerField(default=0, verbose_name="Days the user has been in the system")
#     concierge_call_needed = models.BooleanField(default=False)
#     referral_agent = models.CharField(max_length=255, null=True, blank=True)

#     def __str__(self):
#         return f"Other Info for {self.account.username}"
