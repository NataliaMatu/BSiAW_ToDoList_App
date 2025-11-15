from django.contrib.sessions.models import Session
from django.utils import timezone

class SingleSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        # Jeśli użytkownik jest zalogowany i sygnał ustawił flagę
        if request.user.is_authenticated and request.session.get('kill_old_sessions'):
            current = request.session.session_key

            # Usuń flagę, żeby nie powtarzać
            del request.session['kill_old_sessions']
            request.session.save()

            # Usuń stare sesje tego użytkownika
            sessions = Session.objects.filter(expire_date__gt=timezone.now())

            for s in sessions:
                data = s.get_decoded()
                if data.get('_auth_user_id') == str(request.user.id) and s.session_key != current:
                    s.delete()

        return response
