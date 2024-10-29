from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DetailView
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Team, Membership
from .forms import TeamForm
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated





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
        Membership.objects.create(user=self.request.user, team=self.object, role=Membership.ADMIN)
        
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
        context['is_admin'] = team.is_admin(self.request.user)
        return context








User = get_user_model()

class UserSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, team_id):
        query = request.GET.get('query', '')
        team = Team.objects.get(id=team_id)
        team_members = Membership.objects.filter(team=team).values_list('user_id', flat=True)

        # Filter users: active, not in team, matching query
        users = User.objects.filter(
            Q(username__icontains=query) & Q(is_active=True) & ~Q(id__in=team_members)
        ).exclude(id=request.user.id)

        # Serialize results
        user_data = [{'id': user.id, 'username': user.username} for user in users]
        return Response({'users': user_data})









class AddMemberView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, team_id):
        team = Team.objects.get(id=team_id)
        # Check if the current user is an admin
        if not Membership.objects.filter(user=request.user, team=team, role=Membership.ADMIN).exists():
            return Response({'error': 'Only admins can add members'}, status=status.HTTP_403_FORBIDDEN)

        user_id = request.data.get('user_id')
        user = User.objects.get(id=user_id)
        # Add the user to the team
        Membership.objects.create(user=user, team=team, role=Membership.MEMBER)

        return Response({'success': True, 'message': f'{user.username} added as a member.'})
