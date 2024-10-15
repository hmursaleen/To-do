from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


'''
class Category(models.Model):
    """
    Model representing task categories.
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
'''




class Task(models.Model):
    """
    Model representing a task in the to-do list.
    """

    PRIORITY_CHOICES = [
        ('H', 'High'),
        ('M', 'Medium'),
        ('L', 'Low'),
    ]

    title = models.CharField(max_length=255)  # Title of the task
    description = models.TextField(blank=True, help_text="Optional description of the task")  # Detailed task description
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")  # Task owner (user)
    created_at = models.DateTimeField(auto_now_add=True)  # Time the task was created
    updated_at = models.DateTimeField(auto_now=True)  # Time the task was last updated
    due_date = models.DateTimeField(null=True, blank=True)  # Optional due date for the task
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='M')  # Task priority
    is_completed = models.BooleanField(default=False)  # Completion status of the task
    #category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks")

    class Meta:
        ordering = ['due_date', 'priority', 'created_at']  # Default ordering of tasks
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self):
        return self.title