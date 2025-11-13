from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Todo

@method_decorator(login_required, name='dispatch')
class IndexView(generic.ListView):
    template_name = 'todos/index.html'
    context_object_name = 'todo_list'

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user).order_by('-created_at')

@login_required
def add(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        if title:
            Todo.objects.create(title=title, user=request.user)
    return redirect('todos:index')

@login_required
def delete(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id, user=request.user)
    todo.delete()
    return redirect('todos:index')

@login_required
def update(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id, user=request.user)
    todo.isCompleted = request.POST.get('isCompleted') == 'on'
    todo.save()
    return redirect('todos:index')