from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import LoginView
import json

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

def session_expired(request):
    return render(request, 'session/session_expired.html')
