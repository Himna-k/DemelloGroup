from django.db import models
from django.conf import settings
from . choices import STATE_CHOICES,ENTITY_CHOICES,TITLE_CHOICES,MONTH_CHOICES,YEAR_CHOICES,AMOUNT_CHOICES,INDUSTRY_CHOICES,CREDIT_CHOICES,FREE_EMAIL_DOMAINS
class Business(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="businesses")
    
    # General Business Information
    business_legal_name = models.CharField(max_length=255, default='unknown', null=False, blank=False)
    ein = models.BooleanField(default=False, verbose_name="Does your Business have an EIN?")
    domain_name = models.CharField(max_length=255, blank=True, null=True)

    # Contact Information
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=2, choices=STATE_CHOICES, default='', null=True)

    zip_code = models.CharField(max_length=5, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    business_email = models.EmailField(blank=True, default='NONE', null=True)
    primary_contact_title = models.CharField(max_length=15, choices=TITLE_CHOICES, null=True)
    business_phone = models.CharField(max_length=10, blank=True, default='NONE', null=True)

    # Business Status
    month_started = models.CharField(max_length=10, choices=MONTH_CHOICES, default='NONE', null=True)
    year_started = models.CharField(max_length=4, choices=YEAR_CHOICES, default='NONE', null=True)
    industry_focus = models.CharField(max_length=30, choices=INDUSTRY_CHOICES, default='NONE', null=True)
    business_type = models.CharField(max_length=15, choices=ENTITY_CHOICES, default='NONE', null=True)
    gross_monthly_revenue = models.CharField(max_length=15, choices=AMOUNT_CHOICES, default='NONE', null=True)
    total_monthly_credit_sales = models.CharField(max_length=15, choices=AMOUNT_CHOICES, default='NONE', null=True)
    other_income = models.CharField(max_length=15, choices=AMOUNT_CHOICES, default='NONE', null=True)
    current_purchase_amount = models.CharField(max_length=15, choices=AMOUNT_CHOICES, default='NONE', null=True)
    value_of_other_equipment = models.CharField(max_length=15, choices=AMOUNT_CHOICES, default='NONE', null=True)

    structured_payments = models.BooleanField(default=False)
    real_estate_payments = models.BooleanField(default=False)
    trademark_verified = models.BooleanField(default=False)
    good_standing = models.BooleanField(default=False)

    # Phone & 411
    directory_phone_411 = models.CharField(max_length=10, blank=True, default='', null=True)
    directory_phone_800 = models.CharField(max_length=10, blank=True, default='', null=True)
    submit_info_directory = models.BooleanField(default=False)
    listed_in_411 = models.BooleanField(default=False)
    fax_number = models.CharField(max_length=10, blank=True, null=True)

    # Credit Information
    experian = models.CharField(max_length=10, choices=CREDIT_CHOICES, default='NONE', null=True)
    transunion = models.CharField(max_length=10, choices=CREDIT_CHOICES, default='NONE', null=True)
    equifax = models.CharField(max_length=10, choices=CREDIT_CHOICES, default='NONE', null=True)
    judgments = models.BooleanField(default=False)
    personal_income = models.CharField(max_length=20, blank=True, default='', null=True)
    business_credit_score = models.BooleanField(default=False)

    reporting_trade_lines = models.PositiveIntegerField(default=0)
    bankruptcy = models.BooleanField(default=False)
    
    ein_verified = models.BooleanField(default=False)  # corrected field name
    licenses_obtained = models.BooleanField(default=False)  # corrected field name

    account_linked=models.BooleanField(default=False)
    establish_merchant_account=models.BooleanField(default=False)
    
    business_filing_status=models.BooleanField(default=False)
    country_licence_permit=models.BooleanField(default=False)
    city_licence_permit=models.BooleanField(default=False)
    irs_filings=models.BooleanField(default=False)
    account_status=models.BooleanField(default=False)
    directory_assistance=models.BooleanField(default=False)
    
    business_plan=models.BooleanField(default=False)
    # Compliance check method for Entity and Filings section
    def is_business_email_free(self):
        if self.business_email:
            domain = self.business_email.split('@')[-1]
            return domain in FREE_EMAIL_DOMAINS
        return False
    def entity_compliant(self):
        return bool(self.business_type and self.state and self.trademark_verified and self.good_standing)


    def location_compliant(self):
        return bool(
            self.business_legal_name and
            self.first_name and
            self.last_name and
            self.primary_contact_title and
            self.phone and
            self.address and
            self.city and
            self.zip_code
        )
    def location_compliant(self):
        return bool(
            self.business_legal_name and
            self.first_name and
            self.last_name and
            self.primary_contact_title and
            self.phone and
            self.address and
            self.city and
            self.zip_code
        )
    def phone_compilant(self):
        return bool(
            self.listed_in_411 and
            self.directory_phone_411 and
            self.directory_phone_800
        )
    
    def website_compilant(self):
        return bool(
          self.domain_name and
          self.business_email and
          self.email  
        )
        
    def ein_compliant(self):
        return bool(self.ein_verified and self.licenses_obtained)
    def banking_compilant(self):
        return bool(
            self.account_linked and
            self.establish_merchant_account
        )
    def agencies_compilance(self):
        return bool(
            self.directory_assistance and
            self.account_status and
            self.irs_filings and
            self.city_licence_permit and
            self.country_licence_permit and
            self.business_filing_status
        )
    def has_business_plan(self):
        return bool(
            self.business_plan
        )
    def update_entity_info(self, entity_type, state, trademark_verified, good_standing):
        # Only update fields if they have a valid (non-None) value
        if entity_type:
            self.business_type = entity_type
        if state:
            self.state = state
        self.trademark_verified = trademark_verified  # Boolean fields don't require None checks
        self.good_standing = good_standing

        # Save the updated instance
        self.save()

    def update_location_info(self, business_name, first_name, last_name, contact_title, phone, address, city, state, zip_code):
        if business_name:
            self.business_legal_name = business_name
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        if contact_title:
            self.primary_contact_title = contact_title
        if phone:
            self.phone = phone
        if address:
            self.address = address
        if city:
            self.city = city
        if state:
            self.state = state
        if zip_code:
            self.zip_code = zip_code
        self.save()

        
    def update_phone_info(self, listed_in_411, phone_411, submit_to_411, fax_number, phone_800):
        if phone_411:
            self.directory_phone_411 = phone_411
        if listed_in_411 is not None:  # Boolean fields need only be checked for None
            self.listed_in_411 = listed_in_411
        if phone_800:
            self.directory_phone_800 = phone_800
        if submit_to_411 is not None:  # Boolean fields need only be checked for None
            self.submit_info_directory = submit_to_411
        if fax_number:
            self.fax_number = fax_number
        self.save()

        
    def update_website_info(self, domain_name, business_mail, personal_mail):
        if personal_mail:
            self.email = personal_mail
        if domain_name:
            self.domain_name = domain_name
        if business_mail:
            self.business_email = business_mail
        self.save()
    
    def update_ein_info(self,ein_verified,licenses_obtained):
        self.ein_verified = ein_verified
        self.licenses_obtained = licenses_obtained
        self.save()
        
    def update_banking_info(self,account_linked,establish_merchant_account):
        self.account_linked=account_linked
        self.establish_merchant_account=establish_merchant_account
        self.save()
        
    def update_agencies_info(self,business_filing_status,
        country_licence_permit,
        city_licence_permit,
        irs_filings,
        account_status,
        directory_assistance):
        self.business_filing_status = business_filing_status
        self.country_licence_permit = country_licence_permit
        self.city_licence_permit = city_licence_permit
        self.irs_filings = irs_filings
        self.account_status = account_status    
        self.directory_assistance = directory_assistance
        self.save()
    
    def update_business_plan(self, business_plan):
        """Updates the business_plan field and saves the model."""
        self.business_plan = business_plan
        self.save()

    def __str__(self):
        return f"{self.business_legal_name} (Owned by {self.user.username})"
