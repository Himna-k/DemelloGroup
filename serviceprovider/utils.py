# In serviceprovider/utils.py or wherever these functions are defined

def is_client(user):
    # Check if user is authenticated first
    if not user.is_authenticated:
        return False
    return user.user_type == 'client'

def is_service_provider(user):
    # Check if user is authenticated first
    if not user.is_authenticated:
        return False
    return user.user_type == 'service_provider'
