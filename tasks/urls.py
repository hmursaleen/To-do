from django.urls import path, include
from .views import TaskCreateView

app_name = 'tasks'

urlpatterns = [
    path('create/', TaskCreateView.as_view(), name='task_create'),
    # Other task-related URLs...
]
