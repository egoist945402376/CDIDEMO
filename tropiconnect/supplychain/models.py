from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class FarmerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='farmer_profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField(blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Farm(models.Model):
    farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name='farms')
    farm_name = models.CharField(max_length=200)
    location = models.CharField(max_length=255)
    description = models.TextField()
    established_year = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.farm_name

class FarmPhoto(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to='farm_photos/')
    caption = models.CharField(max_length=255, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Photo for {self.farm.farm_name}"

class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Product Categories"

class FarmerProduct(models.Model):
    farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')
    product_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return self.product_name

class ShippingMethod(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class FarmerShippingMethod(models.Model):
    farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name='shipping_methods')
    shipping_method = models.ForeignKey(ShippingMethod, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.farmer} - {self.shipping_method}"
    
    class Meta:
        unique_together = ('farmer', 'shipping_method')