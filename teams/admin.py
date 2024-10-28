from django.contrib import admin
from .models import Team, Membership

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'created_by')
    search_fields = ('name', 'created_by__username')

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'team', 'role', 'joined_at')
    search_fields = ('user__username', 'team__name')
    list_filter = ('role',)
