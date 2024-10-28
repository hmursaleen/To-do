"""
URL configuration for todo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

# Set up drf-yasg for automatic API documentation
schema_view = get_schema_view(
    openapi.Info(
        title="ToDo API",
        default_version='v1',
        description="API documentation for the ToDo app",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # Include your API app URLs
    path('task/', include('tasks.urls')),
    path('user/', include('users.urls')),
    path('search/', include('search.urls')),
    path('notifications/', include('notifications.urls')),
    path('core/', include('core.urls')),
    path('team/', include('teams.urls', namespace='teams')),

    # drf-yasg routes for Swagger and ReDoc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

'''
drf-yasg: The get_schema_view function is used to generate API documentation. You’ll get two types of documentation:
Swagger UI: View it at /swagger/.
ReDoc UI: View it at /redoc/.
API URLs: The line path('api/', include('api.urls')) includes your API routes from the api/urls.py file.
'''