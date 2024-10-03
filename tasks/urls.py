from django.urls import path, include
from .views import TaskCreateView, TaskListView, TaskUpdateView, TaskDetailView, TaskDeleteView

app_name = 'tasks'

urlpatterns = [
    path('create/', TaskCreateView.as_view(), name='task_create'),
    path('all/', TaskListView.as_view(), name='task_list'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('<int:pk>/detail/', TaskDetailView.as_view(), name='task_detail'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
]
