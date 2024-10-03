from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from .serializers import TaskSerializer
from tasks.models import Task



'''
ViewSet: The ModelViewSet simplifies CRUD operations, following DRY principles.
Permissions & Authentication: Ensures only authenticated users can access and manage their tasks.
ModelViewSet: This viewset handles all CRUD operations (Create, Retrieve, Update, Delete) out of the box.
get_queryset: It limits the tasks returned by the API to those owned by the authenticated user (self.request.user).
perform_create: When creating a task, we automatically set the owner to the currently authenticated user.
permission_classes: We use IsAuthenticated to ensure only logged-in users can access the API.
authentication_classes: Supports session and token-based authentication (you can extend this depending on your project's needs).
'''

class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for performing CRUD operations on Task model.
    Only authenticated users can access and manage their own tasks.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get_queryset(self):
        """
        Returns tasks that belong to the authenticated user.
        """
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """
        Automatically set the task's owner to the current user during creation.
        """
        serializer.save(owner=self.request.user)
