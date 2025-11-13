from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        print("LOGIN form_valid CALLED")
        print("GET:", self.request.GET)
        print("POST:", self.request.POST)

        browser_id = self.request.GET.get("browser_id")

        print("browser_id extracted =", browser_id)

        response = super().form_valid(form)

        if browser_id:
            print("SAVING browser_id as active:", browser_id)
            self.request.session["_browser_id"] = browser_id
            self.request.session.cycle_key()
        else:
            print("!!!!! browser_id MISSING !!!!!")

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
    print("\n### SESSION CHECK CALLED ###")

    if not request.user.is_authenticated:
        print("NOT AUTHENTICATED")
        return JsonResponse({"valid": False})

    data = json.loads(request.body.decode("utf-8"))
    browser_id = data.get("browser_id")
    session_browser_id = request.session.get("_browser_id")

    print("browser_id FROM REQUEST:", browser_id)
    print("ACTIVE browser_id IN SESSION:", session_browser_id)

    # ta karta jest aktywna
    if browser_id == session_browser_id:
        print("VALID → SAME BROWSER")
        return JsonResponse({"valid": True})

    # ta karta jest NIEAKTYWNA → wygasła
    print("INVALID → SESSION EXPIRED FOR THIS TAB")
    return JsonResponse({"valid": False})


def session_expired(request):
    return render(request, 'session/session_expired.html')
