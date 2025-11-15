from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import LoginView
import json


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        browser_id = self.request.POST.get("browser_id")
        response = super().form_valid(form)

        if browser_id:
            self.request.session["_browser_id"] = browser_id
            self.request.session.save()

        return response


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('todos:index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@csrf_exempt
def session_check(request):
    if not request.user.is_authenticated:
        return JsonResponse({"valid": False})

    try:
        data = json.loads(request.body.decode("utf-8"))
    except:
        return JsonResponse({"valid": True})

    browser_id = data.get("browser_id")
    session_browser_id = request.session.get("_browser_id")

    if session_browser_id is None:
        return JsonResponse({"valid": True})

    if session_browser_id == browser_id:
        return JsonResponse({"valid": True})

    return JsonResponse({"valid": False})


def session_expired(request):
    return render(request, 'session/session_expired.html')
