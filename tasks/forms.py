from django import forms
from .models import Task
from django.utils import timezone




'''
Meta class:

model: Specifies the model (Task) this form is based on.
fields: Only the necessary fields are included: title, description, due_date, priority, and is_completed.
widgets: Customizes the form inputs, such as using a datetime-local input for the due date and making the description a textarea.
labels: Custom labels for better user experience.
help_texts: Provides helpful hints for users about what each field represents.
clean_title:

This method ensures that the task's title is not too short (minimum of 3 characters).
clean_due_date:

This method ensures that the due date, if provided, is not in the past. You can use Django's timezone.now() to compare the date.
'''



class TaskForm(forms.ModelForm):
    """
    Form for creating and updating tasks. Based on the Task model.
    """

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'is_completed', 'category', ]
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'category': forms.Select(),  # Ensure the category field uses a select dropdown
        }
        labels = {
            'title': 'Task Title',
            'description': 'Task Description',
            'due_date': 'Due Date',
            'priority': 'Task Priority',
            'is_completed': 'Mark as Completed',
            'category': 'Task Category',
        }
        help_texts = {
            'due_date': 'Set a deadline for this task (optional).',
            'priority': 'Select the importance level of the task.',
            'category': 'Select the category of the task (optional).',
        }

    def clean_title(self):
        """
        Ensure that the title is not empty or too short.
        """
        title = self.cleaned_data.get('title')
        if not title or len(title) < 3:
            raise forms.ValidationError("The title must be at least 3 characters long.")
        return title

    def clean_due_date(self):
        """
        Ensure that the due date is in the future, if provided.
        """
        due_date = self.cleaned_data.get('due_date')
        if due_date and due_date < timezone.now():
            raise forms.ValidationError("The due date cannot be in the past.")
        return due_date
