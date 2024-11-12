from django.urls import path
from . import views
app_name = 'teams'  # Namespace for the teams app

urlpatterns = [
    path('create/', views.TeamCreateView.as_view(), name='team_create'),  # URL for team creation
    path('<int:pk>/', views.TeamDetailView.as_view(), name='team_detail'),  # URL for viewing team details
    path('<int:team_id>/search_user/', views.UserSearchView.as_view(), name='user_search'),
    path('<int:team_id>/add_member/', views.AddMemberView.as_view(), name='add_member'),
    path('<int:team_id>/create-task/', views.TeamTaskCreateView.as_view(), name='create-team-task'),
    path('<int:team_id>/task-list/', views.TeamTaskListView.as_view(), name='team-task-list'),
    path('<int:team_id>/task/<int:pk>/', views.TeamTaskDetailView.as_view(), name='team-task-detail'),
    path('<int:team_id>/task/<int:pk>/assignable_users/', views.AssignableUserSearchView.as_view(), name='assignable_user_search'),
    #path('<int:task_id>/assign_user/', views.AssignUserToTaskView.as_view(), name='assign_user_to_task'),
]