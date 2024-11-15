from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Car, CarImage
from .serializers import CarSerializer, CarImageSerializer, UserSerializer
from django.contrib.auth.models import User
from django.db import transaction

class CarViewSet(viewsets.ModelViewSet):
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        with transaction.atomic():
            car = serializer.save(user=self.request.user)
            images = self.request.FILES.getlist('images')
            for image in images:
                CarImage.objects.create(car=car, image=image)

    def perform_update(self, serializer):
        with transaction.atomic():
            car = serializer.save()
            images = self.request.FILES.getlist('images')
            if images:
                car.images.all().delete()  # Remove existing images if new ones are uploaded
                for image in images:
                    CarImage.objects.create(car=car, image=image)

    def get_queryset(self):
        queryset = Car.objects.filter(user=self.request.user)
        query = self.request.query_params.get('search')
        if query:
            queryset = queryset.filter(title__icontains=query) | queryset.filter(description__icontains=query) | queryset.filter(car_type__icontains=query)
        return queryset


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return super().get_permissions()

    def get_queryset(self):
        if self.action in ['retrieve', 'update', 'destroy']:
            return User.objects.filter(id=self.request.user.id)
        return super().get_queryset()


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

class UpdateProfile(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user
        data = request.data

        # Validate and update the user's data (username, email, password)
        serializer = UserSerializer(user, data=data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)