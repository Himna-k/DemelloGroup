# serviceprovider/models.py
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    user_type = models.CharField(max_length=50, 
                                 choices=(("client", "Client"), ("service_provider", "Service Provider")),default="client" )
class ServiceProviderProfile(models.Model):
    # Temporarily remove the reference to CustomerProfile
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="service_provider_profile")
    company_name = models.CharField(max_length=255, blank=True, null=True)
    business_phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"Service Provider Profile of {self.user}"


# class ServiceProviderCustomerRelation(models.Model):
#     service_provider = models.ForeignKey(ServiceProviderProfile, on_delete=models.CASCADE, related_name='customers')
#     customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='service_providers')

#     def __str__(self):
#         return f"Relation between {self.service_provider.user.username} and {self.customer.user.username}"

# class ServiceProviderDashboard(models.Model):
#     service_provider = models.OneToOneField(ServiceProviderProfile, on_delete=models.CASCADE, related_name="service_provider_dashboard")

#     def __str__(self):
#         return f"Service Provider Dashboard for {self.service_provider.user.username}"






# from django.db import models
# from django.contrib.auth.models import User


# class ServiceProviderProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="service_provider_profile")
#     company_name = models.CharField(max_length=255, blank=True, null=True)
#     business_phone = models.CharField(max_length=15, blank=True, null=True)
    
#     def __str__(self):
#         return f"Service Provider Profile of {self.user.username}"


# class ServiceProviderDashboard(models.Model):
#     service_provider = models.OneToOneField(User, on_delete=models.CASCADE, related_name="service_provider_dashboard")
#     customer_list = models.ManyToOneRel(User, related_name="managed_customers", limit_choices_to={'role': 'customer'})
    
#     def __str__(self):
#         return f"Service Provider Dashboard for {self.service_provider.username}"
