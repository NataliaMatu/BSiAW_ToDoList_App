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

"""
@receiver(user_logged_in)
def kill_other_sessions(sender, user, request, **kwargs):
    if not request.session.session_key:
        request.session.save()
    current_key = request.session.session_key
    SessionModel = get_session_model()
    for s in SessionModel.objects.filter(expire_date__gt=timezone.now()):
        try:
            data = s.get_decoded()
        except Exception:
            continue
        if data.get('_auth_user_id') == str(user.id) and s.session_key != current_key:
            s.delete()
"""