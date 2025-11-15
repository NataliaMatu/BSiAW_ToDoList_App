import time
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.utils import timezone
from importlib import import_module
from django.http import JsonResponse
from django.conf import settings


def get_session_model():
    try:
        mod = import_module('user_sessions.models')
        return getattr(mod, 'Session')
    except Exception:
        from django.contrib.sessions.models import Session
        return Session


GRACE_PERIOD = getattr(settings, "ACTIVE_SESSION_GRACE_PERIOD", 2)


class ActiveSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            return self.get_response(request)

        session_key = request.session.session_key
        if not session_key:
            try:
                request.session.save()
            except Exception:
                return self.get_response(request)
            session_key = request.session.session_key

        SessionModel = get_session_model()

        try:
            if SessionModel.objects.count() == 0:
                return self.get_response(request)
        except Exception:
            return self.get_response(request)

        try:
            sessions = SessionModel.objects.filter(expire_date__gt=timezone.now())
        except Exception:
            return self.get_response(request)

        user_sessions = []
        for s in sessions:
            try:
                data = s.get_decoded()
            except Exception:
                continue
            if data.get('_auth_user_id') == str(request.user.id):
                user_sessions.append(s.session_key)

        if len(user_sessions) == 0:
            return self.get_response(request)

        if session_key in user_sessions:
            return self.get_response(request)

        checked_marker = "_active_session_checked_at"
        now = time.time()
        last_checked = request.session.get(checked_marker)

        if not last_checked:
            request.session[checked_marker] = now
            try:
                request.session.save()
            except Exception:
                pass
            return self.get_response(request)

        if now - last_checked < GRACE_PERIOD:
            return self.get_response(request)

        logout(request)
        xrw = request.META.get("HTTP_X_REQUESTED_WITH", "")
        accepts_json = "application/json" in request.META.get("HTTP_ACCEPT", "")
        if xrw == "XMLHttpRequest" or accepts_json:
            return JsonResponse({"expired": True}, status=200)
        return redirect("session_expired")
