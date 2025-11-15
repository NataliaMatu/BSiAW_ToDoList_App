from django.contrib.auth.signals import user_logged_in
from django.contrib.sessions.models import Session
from django.dispatch import receiver
from django.utils import timezone

print("SIGNAL LOADED")
"""
@receiver(user_logged_in)
def kill_other_sessions(sender, user, request, **kwargs):
    current_session_key = request.session.session_key
    print("SIGNAL FIRED", user.username, current_session_key)
    # wszystkie aktywne sesje
    sessions = Session.objects.filter(expire_date__gt=timezone.now())

    for session in sessions:
        data = session.get_decoded()

        # sesje tego samego użytkownika, ale nie ta nowa
        if data.get('_auth_user_id') == str(user.id) and session.session_key != current_session_key:
            session.delete()
"""

@receiver(user_logged_in)
def mark_for_cleanup(sender, user, request, **kwargs):
    request.session['kill_old_sessions'] = True
