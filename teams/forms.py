from django import forms
from .models import Team, TeamTask
from tasks.forms import TaskForm


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name']
        labels = {
            'name': 'Team Name',
        }
        help_texts = {
            'name': 'Enter a unique name for your team.',
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Team.objects.filter(name=name).exists():
            raise forms.ValidationError("A team with this name already exists.")
        return name









class TeamTaskForm(TaskForm):

    class Meta(TaskForm.Meta):
        model = TeamTask