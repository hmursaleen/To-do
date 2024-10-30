from django.http import JsonResponse
from django.db.models import Q
from django.views.generic import ListView
from tasks.models import Task
from django.contrib.auth.mixins import LoginRequiredMixin




class SearchTask(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        # Get the current user
        user = self.request.user
        queryset = super().get_queryset()

        # Get the search query from the request
        query = self.request.GET.get('query', '')

        # Filter the queryset to include only tasks owned by the current user
        queryset = queryset.filter(owner=user)

        # Apply the search filter if a query is provided
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(category__icontains=query)  # Adjust for ForeignKey relation
            )

        return queryset

    def render_to_response(self, context, **response_kwargs):
        # Check if the request is an AJAX request
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            tasks = self.get_queryset()
            task_list = [{
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'priority': task.priority,
                'due_date': task.due_date.strftime('%Y-%m-%d') if task.due_date else None,
                'category': task.category if task.category else 'Uncategorized',
                'owner': task.owner.username,
            } for task in tasks]

            return JsonResponse({'tasks': task_list})

        return super().render_to_response(context, **response_kwargs)
