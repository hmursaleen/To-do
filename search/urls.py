from django.urls import path
from .views import SearchTask

app_name = 'search'

urlpatterns = [
    path('', SearchTask.as_view(), name='search_tasks'),
]