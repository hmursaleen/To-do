from django.urls import path
from .views import TeamCreateView, TeamDetailView

app_name = 'teams'  # Namespace for the teams app

urlpatterns = [
    path('create/', TeamCreateView.as_view(), name='team_create'),  # URL for team creation
    path('<int:pk>/detail/', TeamDetailView.as_view(), name='team_detail'),  # URL for viewing team details
]
