from django.contrib import admin
from .models import ServiceProviderProfile

@admin.register(ServiceProviderProfile)
class ServiceProviderProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'business_phone')