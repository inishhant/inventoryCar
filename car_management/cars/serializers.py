from rest_framework import serializers
from .models import Car, CarImage
from django.contrib.auth.models import User

class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ['id', 'image']

class CarSerializer(serializers.ModelSerializer):
    images = CarImageSerializer(many=True, required=False)

    class Meta:
        model = Car
        fields = ['id', 'user', 'title', 'description', 'car_type', 'company', 'dealer', 'price', 'images', 'created_at', 'updated_at']
        read_only_fields = ['user']

    def create(self, validated_data):
        images_data = self.context['request'].FILES.getlist('images')
        car = Car.objects.create(**validated_data)
        for image_data in images_data:
            CarImage.objects.create(car=car, image=image_data)
        return car

    def update(self, instance, validated_data):
        images_data = self.context['request'].FILES.getlist('images')
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if images_data:
            instance.images.all().delete()  # Clear old images if new ones are uploaded
            for image_data in images_data:
                CarImage.objects.create(car=instance, image=image_data)
        return instance

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # Create user with hashed password
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        # Update user and handle password hashing
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
            validated_data.pop('password')
        return super().update(instance, validated_data)