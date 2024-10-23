from django import forms

class TaskSearchForm(forms.Form):
    query = forms.CharField(
        label='Search Tasks',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search tasks...'})
    )
