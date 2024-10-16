from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import login
from django.shortcuts import redirect




class CustomLogoutView(LogoutView):
    """
    Custom class-based view for logging out users.
    """
    template_name = 'users/logout_confirmation.html'
    next_page = reverse_lazy('login')  # Redirect to login page after logout
    #next_page: Automatically redirects the user to the login page after they log out.








class CustomLoginView(LoginView):
    """
    Class-based view for user login using the custom authentication form.
    """
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'





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
