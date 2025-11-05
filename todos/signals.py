# todos/signals.py
from importlib import import_module
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone

def get_session_model():
    try:
        mod = import_module('user_sessions.models')
        return getattr(mod, 'Session')
    except Exception:
        from django.contrib.sessions.models import Session as DjangoSession
        return DjangoSession

@receiver(user_logged_in)
def kill_other_sessions(sender, user, request, **kwargs):
    # upewnij się, że sesja ma klucz
    if not request.session.session_key:
        request.session.save()
    current_key = request.session.session_key
    SessionModel = get_session_model()
    active = SessionModel.objects.filter(expire_date__gt=timezone.now())
    for s in active:
        try:
            data = s.get_decoded()
        except Exception:
            data = {}
        if data.get('_auth_user_id') == str(user.id) and getattr(s, 'session_key', None) != current_key:
            s.delete()
