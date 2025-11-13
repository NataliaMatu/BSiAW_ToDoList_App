from django.shortcuts import redirect
from django.contrib.auth import logout
from django.utils import timezone
from importlib import import_module
from django.http import JsonResponse


def get_session_model():
    try:
        mod = import_module('user_sessions.models')
        return getattr(mod, 'Session')
    except:
        from django.contrib.sessions.models import Session
        return Session


class ActiveSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # jeśli nie zalogowany → nie sprawdzamy nic
        if not request.user.is_authenticated:
            return self.get_response(request)

        session_key = request.session.session_key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key

        SessionModel = get_session_model()

        sessions = SessionModel.objects.filter(expire_date__gt=timezone.now())

        user_sessions = []
        for s in sessions:
            try:
                data = s.get_decoded()
            except:
                continue
            if data.get('_auth_user_id') == str(request.user.id):
                user_sessions.append(s.session_key)

        if session_key not in user_sessions:
            logout(request)
            xrw = request.META.get("HTTP_X_REQUESTED_WITH", "")
            accepts_json = "application/json" in request.META.get("HTTP_ACCEPT", "")
            if xrw == "XMLHttpRequest" or accepts_json:
                return JsonResponse({"expired": True}, status=200)
            return redirect("session_expired")

        return self.get_response(request)
