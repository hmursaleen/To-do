from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DetailView, ListView
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from .models import Team, TeamTask, Membership
from .forms import TeamForm, TeamTaskForm
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponseForbidden
from tasks.models import Task
from django.http import JsonResponse
from tasks.views import TaskListView
from search.views import SearchTask
from api.serializers import TaskSerializer
from django.shortcuts import get_object_or_404, redirect






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
        
        # Retrieve members and determine if the user is an admin
        membership = Membership.objects.filter(user=self.request.user, team=team).first()
        context['members'] = Membership.objects.filter(team=team).select_related('user')
        context['is_admin'] = membership.is_admin() if membership else False
        
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









class TeamTaskCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating a task within a specific team.
    Only team admins are allowed to create tasks for the team.
    """
    model = TeamTask
    form_class = TeamTaskForm
    template_name = 'tasks/task_form.html'

    def dispatch(self, request, *args, **kwargs):
        # Get the team instance
        self.team = get_object_or_404(Team, id=kwargs['team_id'])

        # Check if the user is a team admin
        membership = Membership.objects.filter(user=self.request.user, team=self.team).first()
        if not membership or not membership.is_admin():
            return HttpResponseForbidden("You are not authorized to create tasks for this team.")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Set the team field to associate the task with the correct team
        form.instance.team = self.team

        # Save the form and add the user as the task owner
        response = super().form_valid(form)
        form.instance.owner.add(self.request.user)  # Many-to-many field for task owners
        return response

    def get_success_url(self):
        # Redirect to the team detail page after task creation
        return reverse_lazy('teams:team-task-list', kwargs={'team_id': self.team.id})

    def get_context_data(self, **kwargs):
        # Pass additional context for template rendering
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Create Team Task"
        context['header_text'] = f"Create Task for {self.team.name}"
        context['button_text'] = "Create Task"
        return context










class TeamTaskListView(TaskListView, SearchTask, LoginRequiredMixin):
    template_name = 'teams/team_task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        user = self.request.user
        team_id = self.kwargs['team_id']
        team = Team.objects.get(id=team_id)

        # Check user's role in the team
        try:
            membership = team.memberships.get(user=user)
        except Membership.DoesNotExist:
            return TeamTask.objects.none()  # No tasks if user is not a member of the team

        # Admins see all team tasks; members see only their assigned tasks
        queryset = TeamTask.objects.filter(team=team)
        if membership.is_admin():
            pass  # Admin sees all tasks
        else:
            queryset = queryset.filter(owner=user)  # Members see only their tasks

        # Apply filters similar to TaskListView
        category = self.request.GET.get('category')
        priority = self.request.GET.get('priority')
        deadline_order = self.request.GET.get('deadline_order')
        is_completed = self.request.GET.get('is_completed')

        if category:
            queryset = queryset.filter(category=category)
        if priority:
            queryset = queryset.filter(priority=priority)
        if is_completed == 'completed':
            queryset = queryset.filter(is_completed=True)
        elif is_completed == 'not_completed':
            queryset = queryset.filter(is_completed=False)

        if deadline_order == 'asc':
            queryset = queryset.order_by('due_date')
        elif deadline_order == 'desc':
            queryset = queryset.order_by('-due_date')

        # Search logic from SearchTask view if a search query is provided
        query = self.request.GET.get('query', '')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(category__icontains=query)
            )

        return queryset

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            tasks = self.get_queryset()
            task_list = [{
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'priority': task.priority,
                'due_date': task.due_date.strftime('%Y-%m-%d') if task.due_date else None,
                'category': task.category if task.category else 'Uncategorized',
                'owners': [owner.username for owner in task.owner.all()],
            } for task in tasks]
            return JsonResponse({'tasks': task_list})

        return super().render_to_response(context, **response_kwargs)

    
    def get_context_data(self, **kwargs):
        # Customize the context for the team-specific task creation
        context = super().get_context_data(**kwargs)
        team_id = self.kwargs['team_id']
        team = Team.objects.get(id=team_id)
        context['team'] = team
        return context









class TeamTaskDetailView(DetailView):
    model = TeamTask
    template_name = "teams/team_task_detail.html"
    context_object_name = "task"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()
        team_id = self.kwargs['team_id']
        team = Team.objects.get(id=team_id)
        context['team'] = team # Assuming the team is fetched as part of request

        # Get users already assigned to the task
        assigned_users = task.owner.all()
        context['assigned_users'] = assigned_users

        # Check if the user is an admin to conditionally render the search
        membership = Membership.objects.filter(user=self.request.user, team=team).first()
        context['is_admin'] = membership.is_admin() if membership else False

        return context

# Dynamic search for team members to assign to the task
class AssignableUserSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, team_id, pk):
        query = request.GET.get('query', '')
        team = get_object_or_404(Team, id=team_id)
        task = get_object_or_404(Task, id=pk)

        # Members of the team not yet assigned to the task and matching the query
        unassigned_users = User.objects.filter(
            Q(username__icontains=query),
            Q(is_active=True),
            Q(team_memberships__team=team),
        ).exclude(id__in=task.owner.values_list('id', flat=True))

        # Serialize user data for JSON response
        user_data = [{'id': user.id, 'username': user.username} for user in unassigned_users]
        return Response({'users': user_data})