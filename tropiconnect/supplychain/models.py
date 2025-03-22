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
    photo = models.ImageField(upload_to='farm_product_photos/', null=True, blank=True)
    
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


class FarmerCertification(models.Model):
    farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name='certifications')
    certification_name = models.CharField(max_length=200, verbose_name="Certification Name")
    issuing_organization = models.CharField(max_length=200, verbose_name="Issuing Organization")
    issue_date = models.DateField(verbose_name="Issue Date")
    expiry_date = models.DateField(null=True, blank=True, verbose_name="Expiry Date")
    certificate_image = models.ImageField(upload_to='farmer_certifications/', null=True, blank=True,verbose_name="Certificate Image")
    description = models.TextField(blank=True, verbose_name="Description")
    date_added = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-issue_date']
        verbose_name = "Farmer Certification"
        verbose_name_plural = "Farmer Certifications"
    
    def __str__(self):
        return f"{self.certification_name} - {self.farmer.first_name} {self.farmer.last_name}"
    
    def is_valid(self):
        """Check if the certification is still valid based on expiry date"""
        if not self.expiry_date:
            return True
        return self.expiry_date >= timezone.now().date()


class BuyerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='buyer_profile')
    phone_number = models.CharField(max_length=20)
    company_name = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    introduction = models.TextField(help_text="Introduce your company and describe your main agricultural interests")
    date_joined = models.DateTimeField(default=timezone.now)
    company_logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    website = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.company_name

class ProductNeed(models.Model):
    UNIT_CHOICES = [
        ('kg', 'Kilogram'),
        ('ton', 'Metric Ton'),
        ('lb', 'Pound'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('fulfilled', 'Fulfilled'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]
    
    buyer = models.ForeignKey(BuyerProfile, on_delete=models.CASCADE, related_name='product_needs')
    product_category = models.ForeignKey('ProductCategory', on_delete=models.PROTECT)
    product_name = models.CharField(max_length=200)
    description = models.TextField()
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='kg')
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price offered per kilogram in USD")
    date_posted = models.DateTimeField(auto_now_add=True)
    date_needed_by = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    
    def __str__(self):
        return f"{self.product_name} - {self.quantity} {self.unit} - {self.buyer.company_name}"
    
    class Meta:
        ordering = ['-date_posted']
        verbose_name = "Product Need"
        verbose_name_plural = "Product Needs"

class BuyerInterest(models.Model):
    buyer = models.ForeignKey(BuyerProfile, on_delete=models.CASCADE, related_name='interests')
    category = models.ForeignKey('ProductCategory', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.buyer.company_name} - {self.category.name}"
    
    class Meta:
        unique_together = ('buyer', 'category')
        verbose_name = "Buyer Interest"
        verbose_name_plural = "Buyer Interests"