from django.conf import settings
from django.db import models

class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )
    
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    # Indexes to optimize querying
    class Meta:
        indexes = [
            models.Index(fields=['user', 'is_read']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:20]}"

    def mark_as_read(self):
        self.is_read = True
        self.save()
