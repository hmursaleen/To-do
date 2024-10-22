from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Task(models.Model):
    """
    Model representing a task in the to-do list.
    """

    PRIORITY_CHOICES = [
        ('H', 'High'),
        ('M', 'Medium'),
        ('L', 'Low'),
    ]

    CATEGORY_CHOICES = [
        ('Work', 'Work'),
        ('Home', 'Home'),
        ('Personal', 'Personal'),
        ('Other', 'Other'),
    ]

    title = models.CharField(max_length=255)  # Title of the task
    description = models.TextField(blank=True, help_text="Optional description of the task")  # Detailed task description
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")  # Task owner (user)
    created_at = models.DateTimeField(auto_now_add=True)  # Time the task was created
    updated_at = models.DateTimeField(auto_now=True)  # Time the task was last updated
    due_date = models.DateTimeField(null=True, blank=True)  # Optional due date for the task
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='M')  # Task priority
    is_completed = models.BooleanField(default=False)  # Completion status of the task
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, null=True, blank=True)  # Task category

    class Meta:
        ordering = ['-created_at', 'due_date', 'priority', ]  # Default ordering of tasks
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self):
        return self.title
