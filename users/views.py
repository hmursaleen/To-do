from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect

class SignupView(CreateView):
    """
    Class-based view for user registration using the custom signup form.
    """
    form_class = CustomUserCreationForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('tasks:task_list')  # Redirect to task list after successful signup

    def form_valid(self, form):
        response = super().form_valid(form)
        # Automatically log in the user after successful signup
        user = form.save()
        login(self.request, user)
        return response
        '''
        form_valid: After the user is successfully created, it logs in the user automatically using login.
        '''
