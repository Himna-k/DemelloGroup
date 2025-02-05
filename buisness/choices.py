from datetime import datetime

current_year = datetime.now().year
YEAR_CHOICES = [ (str(year),str(year)) for year in range( current_year,1900,-1)]
CREDIT_CHOICES=[ (str(credit),str(credit)) for credit in range( 300,810,10)]

PERSONAL_INCOME_CHOICES = [
    ('', 'Select'),
    ('5k - 10k', '5k - 10k'),
    ('10k - 25k', '10k - 25k'),
    ('25k - 50k', '25k - 50k'),
    ('50k - 75k', '50k - 75k'),
    ('75k - 100k', '75k - 100k'),
    ('100k - 125k', '100k - 125k'),
    ('125k - 150k', '125k - 150k'),
    ('150k - 175k', '150k - 175k'),
    ('175k - 200k', '175k - 200k'),
    ('200k - 225k', '200k - 225k'),
    ('225k - 250k', '225k - 250k'),
    ('250k - 275k', '250k - 275k'),
    ('275k - 300k', '275k - 300k'),
    ('Over 300k', 'Over 300k')
]


AMOUNT_CHOICES = [('', '-- Click To Select --')]

# Adding values from $0 to $100,000 in increments of $2,500
for amount in range(0, 100001, 2500):
    AMOUNT_CHOICES.append((f"${amount:,}", f"${amount:,}"))

# Adding larger increments from $125,000 to $500,000
for amount in range(125000, 500001, 25000):
    AMOUNT_CHOICES.append((f"${amount:,}", f"${amount:,}"))

# Adding values from $750,000 to $5,000,000 in increments of $250,000
for amount in range(750000, 5000001, 250000):
    AMOUNT_CHOICES.append((f"${amount:,}", f"${amount:,}"))

# Adding values from $10,000,000 to $300,000,000 in increments of $5,000,000
for amount in range(10000000, 300000001, 5000000):
    AMOUNT_CHOICES.append((f"${amount:,}", f"${amount:,}"))

INDUSTRY_CHOICES = [
    ('', '-- Click Here To Select --'),
    ('Accounting(CPA)', 'Accounting(CPA)'),
    ('Aerospace', 'Aerospace'),
    ('Agricultural', 'Agricultural'),
    ('Aircraft', 'Aircraft'),
    ('Apparel', 'Apparel'),
    ('Architect', 'Architect'),
    ('Attorney', 'Attorney'),
    ('Automotive Parts', 'Automotive Parts'),
    ('Automotive Service', 'Automotive Service'),
    ('Banking', 'Banking'),
    ('Bed & Breakfast', 'Bed & Breakfast'),
    ('Beverage', 'Beverage'),
    ('Biotech', 'Biotech'),
    ('Chiropractor', 'Chiropractor'),
    ('Clothing Distributor', 'Clothing Distributor'),
    ('Clothing Manufacturer', 'Clothing Manufacturer'),
    ('Computer Hardware', 'Computer Hardware'),
    ('Computer Software', 'Computer Software'),
    ('Construction', 'Construction'),
    ('Consulting', 'Consulting'),
    ('Consumer Products', 'Consumer Products'),
    ('Contractor', 'Contractor'),
    ('Convenience Store (No Gas)', 'Convenience Store (No Gas)'),
    ('Convenience Store (With Gas)', 'Convenience Store (With Gas)'),
    ('Couriers/Messengers', 'Couriers/Messengers'),
    ('Defense', 'Defense'),
    ('Dental Technology', 'Dental Technology'),
    ('Dentist', 'Dentist'),
    ('Distribution/Distributor', 'Distribution/Distributor'),
    ('Education Related', 'Education Related'),
    ('Electronics', 'Electronics'),
    ('Energy', 'Energy'),
    ('Entertainment', 'Entertainment'),
    ('Environmental', 'Environmental'),
    ('Existing Technology', 'Existing Technology'),
    ('Federal Government', 'Federal Government'),
    ('Film, Play, Video', 'Film, Play, Video'),
    ('Financial Services', 'Financial Services'),
    ('Fitness', 'Fitness'),
    ('Food Service', 'Food Service'),
    ('Forestry and Fishing', 'Forestry and Fishing'),
    ('Funeral Home', 'Funeral Home'),
    ('Gaming', 'Gaming'),
    ('Garment', 'Garment'),
    ('Gasoline Station', 'Gasoline Station'),
    ('Government Contracting', 'Government Contracting'),
    ('Health Products', 'Health Products'),
    ('Healthcare', 'Healthcare'),
    ('Hi-Technology', 'Hi-Technology'),
    ('Import/Export', 'Import/Export'),
    ('Industrial Products', 'Industrial Products'),
    ('Insurance', 'Insurance'),
    ('Internet/Online Services', 'Internet/Online Services'),
    ('Legal Profession', 'Legal Profession'),
    ('Lodging', 'Lodging'),
    ('Manufacturing', 'Manufacturing'),
    ('Marine', 'Marine'),
    ('Marketing', 'Marketing'),
    ('Media Production', 'Media Production'),
    ('Medical ("ologists")', 'Medical ("ologists")'),
    ('Medical (licensed)', 'Medical (licensed)'),
    ('Medical (therapists)', 'Medical (therapists)'),
    ('Medical Technology', 'Medical Technology'),
    ('Mobile Home Parks', 'Mobile Home Parks'),
    ('Mortician', 'Mortician'),
    ('Municipal', 'Municipal'),
    ('Natural resources', 'Natural resources'),
    ('New Technology', 'New Technology'),
    ('Optometry', 'Optometry'),
    ('Pharmacist', 'Pharmacist'),
    ('Pharmaceuticals', 'Pharmaceuticals'),
    ('Piece Goods', 'Piece Goods'),
    ('Printing', 'Printing'),
    ('Publishing', 'Publishing'),
    ('Real Estate Related', 'Real Estate Related'),
    ('Resorts', 'Resorts'),
    ('Restaurant', 'Restaurant'),
    ('Retail', 'Retail'),
    ('Retail Distribution', 'Retail Distribution'),
    ('Retail Manufacturing', 'Retail Manufacturing'),
    ('Security', 'Security'),
    ('Semiconductors', 'Semiconductors'),
    ('Service', 'Service'),
    ('Space Technology', 'Space Technology'),
    ('Staffing', 'Staffing'),
    ('Sub-Contractor', 'Sub-Contractor'),
    ('Telecommunications', 'Telecommunications'),
    ('Textiles', 'Textiles'),
    ('Titled Vehicles', 'Titled Vehicles'),
    ('Transportation', 'Transportation'),
    ('Trucking', 'Trucking'),
    ('Veterinary Technology', 'Veterinary Technology'),
    ('Veterinarian', 'Veterinarian'),
    ('Warehousing/Storage', 'Warehousing/Storage'),
    ('Waste or Recycling', 'Waste or Recycling'),
    ('Wholesale', 'Wholesale'),
    ('Other (Not on this list)', 'Other (Not on this list)'),
]


STATE_CHOICES = [
    ('', 'Select a state'),
    ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'),
    ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('FL', 'Florida'), ('GA', 'Georgia'),
    ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'),
    ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'),
    ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'),
    ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'),
    ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'),
    ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('DC', 'Washington, DC'), ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'), ('WY', 'Wyoming')
]

# Define entity choices
ENTITY_CHOICES = [
    ('NONE', 'None Yet'), ('C_CORP', 'C-Corporation'), ('LLC', 'LLC'), ('LLP', 'LLP'),
    ('NON_PROFIT', 'Non-Profit Organization'), ('PARTNERSHIP', 'Partnership'),
    ('PC', 'Professional Corporation (PC)'), ('PRO_CORP', 'Professional Corporation'),
    ('PUBLIC', 'Public Company'), ('S_CORP', 'S-Corporation'), ('SOLE_PROP', 'Sole Proprietor'),
    ('GOV', 'Government'), ('OTHER', 'Other (not Listed)')
]

# Define title choices
TITLE_CHOICES = [
    ('', '-- Click Here To Select --'),
    ('CEO', 'CEO'),
    ('President', 'President'),
    ('Owner', 'Owner'),
    ('Partner', 'Partner'),
    ('CFO', 'CFO'),
    ('CIO', 'CIO'),
    ('COO', 'COO'),
    ('CTO', 'CTO'),
    ('VP', 'VP'),
    ('Director', 'Director'),
    ('Manager', 'Manager'),
    ('Agent', 'Agent'),
    ('Representative', 'Representative'),
    ('Other', 'Other'),
]
MONTH_CHOICES=[('Jan','january'),
    ('Feb','february'),
    ('Mar','march'),
    ('Apr','april'),
    ('May','may'),
    ('Jun','june'),
    ('Jul','july'),
    ('Aug','august'),
    ('Sep','september'),
    ('Oct','october'),
    ('Nov','november'),
    ('Dec','december')]
FREE_EMAIL_DOMAINS = ['gmail.com', 'yahoo.com', 'hotmail.com', 'aol.com', 'msn.com', 'outlook.com', 'icloud.com']
PRICE_LISTS = [
    (0, '$0'),
    (2500, '$2,500'),
    (5000, '$5,000'),
    (7500, '$7,500'),
    (10000, '$10,000'),
    (20000, '$20,000'),
    (30000, '$30,000'),
    (40000, '$40,000'),
    (50000, '$50,000'),
    (60000, '$60,000'),
    (70000, '$70,000'),
    (80000, '$80,000'),
    (90000, '$90,000'),
    (100000, '$100,000'),
    (110000, '$110,000'),
    (120000, '$120,000'),
    (130000, '$130,000'),
    (140000, '$140,000'),
    (150000, '$150,000'),
    (160000, '$160,000'),
    (170000, '$170,000'),
    (180000, '$180,000')
]
