from django.urls import path
from .views import TeamCreateView, TeamDetailView, UserSearchView, AddMemberView, TeamTaskCreateView, TeamTaskListView

app_name = 'teams'  # Namespace for the teams app

urlpatterns = [
    path('create/', TeamCreateView.as_view(), name='team_create'),  # URL for team creation
    path('<int:pk>/', TeamDetailView.as_view(), name='team_detail'),  # URL for viewing team details
    path('<int:team_id>/search_user/', UserSearchView.as_view(), name='user_search'),
    path('<int:team_id>/add_member/', AddMemberView.as_view(), name='add_member'),
    path('<int:team_id>/create-task/', TeamTaskCreateView.as_view(), name='create-team-task'),
    path('<int:team_id>/task-list/', TeamTaskListView.as_view(), name='team-task-list'),
]