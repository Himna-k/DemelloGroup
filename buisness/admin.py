from django.contrib import admin
from clients.models import CustomerProfile, AccountInfo, OtherInfo  # Import from clients.models
from .models import Client, Business

admin.site.register(Client)
admin.site.register(Business)
admin.site.register(CustomerProfile)  # Register CustomerProfile
admin.site.register(AccountInfo)
admin.site.register(OtherInfo)
