"""
URL configuration for car_management project.

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
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.conf import settings
from django.conf.urls.static import static

# Set up Swagger schema view
schema_view = get_schema_view(
    openapi.Info(
        title="Car API",
        default_version='v1',
        description="API documentation for the Car inventory app",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@carapi.local"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,  # Make the documentation publicly available
    permission_classes=(permissions.AllowAny,),  # Allow any user (authenticated or not) to access the docs
)
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('api/', include('cars.urls')),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='api-docs'),  # Swagger UI
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
