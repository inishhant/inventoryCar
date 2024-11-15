from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CarViewSet, UserViewSet, MeView, UpdateProfile

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'cars', CarViewSet, basename='car')

urlpatterns = [
    path('', include(router.urls)),
    path('me/', MeView.as_view(), name='me'),  # Add this line
    path('update-profile/', UpdateProfile.as_view(), name='update-profile'),  # Add this line
]
