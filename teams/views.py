from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DetailView
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Team, Membership
from .forms import TeamForm
from django.shortcuts import get_object_or_404



class TeamCreateView(LoginRequiredMixin, CreateView):
    model = Team
    form_class = TeamForm
    context_object_name = 'team'
    template_name = 'teams/team_create.html'
    
    def form_valid(self, form):
        # Assign the current user as the team creator
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        
        # Create initial Membership entry for the admin role
        Membership.objects.create(user=self.request.user, team=self.object, role=Membership.Role.ADMIN)
        
        # Add a success message
        messages.success(self.request, 'Team created successfully! You are now the admin of the team.')
        
        return response

    def get_success_url(self):
        # Redirect to the team detail view
        return reverse_lazy('teams:team_detail', kwargs={'pk': self.object.pk})








class TeamDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Team
    template_name = 'teams/team_detail.html'
    context_object_name = 'team'
    
    def test_func(self):
        """Check if the user is a member of the team to access the page."""
        team = self.get_object()
        return Membership.objects.filter(user=self.request.user, team=team).exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = self.get_object()
        
        # Add additional context for team members and roles
        context['members'] = Membership.objects.filter(team=team).select_related('user')
        return context
