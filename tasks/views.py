from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from .models import Task
from .forms import TaskForm




'''
Mixins:

LoginRequiredMixin: Ensures that only authenticated users can access this view. If a user isn't logged in, they will be redirected to the login page.
form_class:

This is the form (TaskForm) that will be used to render the form fields and validate input data.
success_url:

Specifies where the user is redirected after successfully creating a task. We're using reverse_lazy('task_list') to lazily resolve the URL for the task list view.
form_valid method:

This method is overridden to set the owner of the task to the current logged-in user before saving the task.
get_context_data:

This method is used to pass extra context (like the page title) to the template, which can enhance the user experience.

'''


class TaskCreateView(CreateView):
    """
    View to handle task creation. Requires login and uses TaskForm.
    """
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')  # Redirect to task list after successful creation

    def form_valid(self, form):
        """
        Override form_valid to associate the task with the logged-in user (owner).
        """
        form.instance.owner = self.request.user  # Set the owner of the task
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Provide additional context to the template, if needed.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create a New Task'
        return context
