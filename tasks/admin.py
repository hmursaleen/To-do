from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'priority', 'is_completed', 'due_date', 'created_at', 'updated_at')
    list_filter = ('priority', 'is_completed', 'owner')
    search_fields = ('title', 'description')
    ordering = ('due_date', 'priority', 'created_at')
