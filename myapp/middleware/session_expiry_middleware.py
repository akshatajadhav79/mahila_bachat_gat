from django.utils import timezone

class SessionExpiryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Update session expiry time on each request
        if request.session.get('_session_expiry_timestamp'):
            expiry_age = request.session.get_expiry_age()
            request.session['_session_expiry_timestamp'] = int(timezone.now().timestamp()) + expiry_age
        else:
            request.session['_session_expiry_timestamp'] = int(timezone.now().timestamp()) + request.session.get_expiry_age()

        response = self.get_response(request)
        return response