from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView


class MarkNotificationAsReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, notification_id):
        try:
            notification = Notification.objects.get(id=notification_id, user=request.user)
            notification.is_read = True
            notification.save()
            return Response({'success': True}, status=200)
        except Notification.DoesNotExist:
            return Response({'error': 'Notification not found'}, status=404)







class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = "notifications/notification_list.html"
    context_object_name = "notifications"
    paginate_by = 10  # Number of notifications per page

    def get_queryset(self):
        """
        Retrieve notifications for the logged-in user.
        Supports filtering for unread notifications via query parameter.
        """
        queryset = Notification.objects.filter(user=self.request.user).order_by("-created_at")
        
        # Filter for unread notifications if 'unread=true' is passed in the query parameters
        unread_filter = self.request.GET.get("unread", None)
        if unread_filter == "true":
            queryset = queryset.filter(is_read=False)

        return queryset