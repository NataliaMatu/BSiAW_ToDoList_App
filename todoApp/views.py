from django.shortcuts import redirect
from django.shortcuts import render
from django.http import JsonResponse

def index(request):
    return redirect('/todos')

def session_expired(request):
    return render(request, 'session/session_expired.html')

def custom_csrf_failure_view(request, reason=""):
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"expired": True})
    return redirect("session_expired")