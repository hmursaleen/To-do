from django.urls import path, include
from .views import TaskCreateView, TaskListView

app_name = 'tasks'

urlpatterns = [
    path('create/', TaskCreateView.as_view(), name='task_create'),
    path('all/', TaskListView.as_view(), name='task_list'),
]
