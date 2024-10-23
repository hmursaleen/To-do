from django.http import JsonResponse
from django.db.models import Q
from django.views.generic import ListView
from tasks.models import Task
from .forms import TaskSearchForm

class SearchTask(ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('query', '')

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(category__icontains=query)  # Fix for ForeignKey relation
            )

        return queryset

    def render_to_response(self, context, **response_kwargs):
        # Check if the request is an AJAX request
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            tasks = self.get_queryset()
            task_list = [{
                'title': task.title,
                'description': task.description,
                'category': task.category if task.category else 'Uncategorized',
            } for task in tasks]

            return JsonResponse({'tasks': task_list})

        return super().render_to_response(context, **response_kwargs)
