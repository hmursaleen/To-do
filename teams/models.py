from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Team(models.Model):
    # Fields
    name = models.CharField(max_length=100, unique=True, verbose_name="Team Name")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_teams",
        verbose_name="Team Admin"
    )

    # Metadata
    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"
        ordering = ['name']  # Alphabetical ordering

    # String Representation
    def __str__(self):
        return self.name







class Membership(models.Model):
    # Role choices as constants
    ADMIN = 'admin'
    MEMBER = 'member'
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (MEMBER, 'Member'),
    ]

    # Fields
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="team_memberships", verbose_name="User")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="memberships", verbose_name="Team")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=MEMBER, verbose_name="Role")
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name="Joined At")

    # Metadata
    class Meta:
        verbose_name = "Membership"
        verbose_name_plural = "Memberships"
        unique_together = ('user', 'team')  # Ensure unique memberships
        #unique_together prevents the same user from being added to the same team multiple times.
        ordering = ['team', 'role']  # Order by team and role for easier management

    # String Representation
    def __str__(self):
        return f"{self.user.username} in {self.team.name} as {self.role}"

    # Helper methods for permissions
    def is_admin(self):
        return self.role == self.ADMIN
