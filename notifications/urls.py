from django.urls import path
from . import views

app_name = "notifications"

urlpatterns = [
    path('<int:notification_id>/mark_as_read/', views.MarkNotificationAsReadView.as_view(), name='mark-as-read'),
    path('all/', views.NotificationListView.as_view(), name="notification_list"),

]
