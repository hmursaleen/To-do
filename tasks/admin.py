from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'priority', 'is_completed', 'due_date', 'created_at', 'updated_at', 'category')
    list_filter = ('priority', 'is_completed', 'owner', 'category')
    search_fields = ('title', 'description')
    ordering = ('due_date', 'priority', 'created_at')
