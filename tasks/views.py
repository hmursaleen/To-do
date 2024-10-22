from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView
from django.views.generic import ListView, UpdateView, DetailView, DeleteView
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


class TaskCreateView(LoginRequiredMixin, CreateView): #
    """
    View to handle task creation. Requires login and uses TaskForm.
    """
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:task-list')  # Redirect to task list after successful creation

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
        context['form_title'] = 'Create Task'
        context['header_text'] = 'Create Task'
        context['button_text'] = 'Create Task'
        return context



'''
get_queryset():

This method filters the tasks to show only the tasks that belong to the logged-in user. Tasks are ordered by their creation date in descending order.
Pagination:

By setting paginate_by = 10, we limit the number of tasks shown per page to 10, which can help in handling large sets of data.
Context Data:

The get_context_data method passes additional context to the template, such as the page title.
'''






class TaskDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView): 
    """
    View to display task details.
    Only the task's owner can view the task details.
    """
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'

    def test_func(self):
        """
        Ensure that only the owner of the task can view it.
        """
        task = self.get_object()
        return task.owner == self.request.user








class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 10  # Optional: Pagination

    def get_queryset(self):
        # Get tasks for the logged-in user
        queryset = Task.objects.filter(owner=self.request.user)
        
        # Get the category from the URL query parameter
        category = self.request.GET.get('category')

        if category:
            # Filter tasks by the selected category
            queryset = queryset.filter(category=category)

        return queryset.order_by('-created_at', 'due_date', 'priority', )  # Apply ordering

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add the available categories to the context
        context['categories'] = Task.CATEGORY_CHOICES

        # Add the selected category (if any) to highlight in the template
        context['selected_category'] = self.request.GET.get('category', '')
        
        return context









class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): # 
    """
    View to update a task. Only the owner of the task can update it.
    Uses LoginRequiredMixin to ensure only logged-in users can access,
    and UserPassesTestMixin to ensure only the task owner can update.
    """
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'  # Use the same form template for creation and update
    success_url = reverse_lazy('tasks:task-list')  # Redirect to task list on success

    def form_valid(self, form):
        """
        Called when a valid form is submitted.
        Optionally, add extra logic here before saving the form.
        """
        return super().form_valid(form)

    def test_func(self):
        """
        Ensure that only the owner of the task can edit it.
        """
        task = self.get_object()
        return task.owner == self.request.user


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Update Task'
        context['header_text'] = 'Update Task'
        context['button_text'] = 'Update Task'
        return context








class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView): #
    """
    View to handle task deletion.
    Only the task's owner can delete the task.
    """
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('tasks:task-list')

    def test_func(self):
        """
        Ensure that only the owner of the task can delete it.
        """
        task = self.get_object()
        return task.owner == self.request.user


'''
success_url: After successful deletion, the user is redirected to the task list page (task_list), which is defined by the URL name 'task_list'.
reverse_lazy: It is used to lazily evaluate the URL reversal. This is preferred in class-based views since the URL isn't resolved until the view is called.
'''