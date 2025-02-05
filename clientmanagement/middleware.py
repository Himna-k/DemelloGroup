from django.shortcuts import redirect
from django.urls import resolve

class RedirectBasedOnProfileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            current_path = resolve(request.path).url_name

            if hasattr(request.user, 'customer_profile'):
                if current_path not in ['clientindex', 'logout', 'signup', 'login']:
                    return redirect('clientindex')

            elif hasattr(request.user, 'service_provider_profile'):
                if current_path not in ['index', 'logout', 'signup', 'login']:
                    return redirect('index')

        return self.get_response(request)
