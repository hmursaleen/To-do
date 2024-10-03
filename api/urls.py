'''
register the viewset with DRF’s router:
'''

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
]

'''
DefaultRouter: Automatically generates URL patterns for the viewset. This approach is clean and follows best practices for REST API routing.
The basename is set to task for URL identification.
'''
