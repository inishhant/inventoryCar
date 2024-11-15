from django.db import models
from django.contrib.auth.models import User

class Car(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars')
    title = models.CharField(max_length=255)
    description = models.TextField()
    car_type = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    dealer = models.CharField(max_length=100)
    price = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='car_images/')

    def __str__(self):
        return f"Image for {self.car.title}"
