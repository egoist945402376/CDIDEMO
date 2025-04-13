from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class FarmerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='farmer_profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField(blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    region = models.CharField(max_length=100, default="Kenya")
    
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


class CompanyCertification(models.Model):
    buyer = models.ForeignKey(BuyerProfile, on_delete=models.CASCADE, related_name='certifications')
    certification_name = models.CharField(max_length=200, verbose_name="Certification Name")
    issuing_organization = models.CharField(max_length=200, verbose_name="Issuing Organization")
    issue_date = models.DateField(verbose_name="Issue Date")
    expiry_date = models.DateField(null=True, blank=True, verbose_name="Expiry Date")
    certificate_image = models.ImageField(upload_to='company_certifications/', null=True, blank=True, verbose_name="Certificate Image")
    description = models.TextField(blank=True, verbose_name="Description")
    date_added = models.DateTimeField(default=timezone.now)
    certification_number = models.CharField(max_length=100, blank=True, verbose_name="Certification Number")
    certification_type = models.CharField(max_length=100, blank=True, verbose_name="Certification Type")
    
    class Meta:
        ordering = ['-issue_date']
        verbose_name = "Company Certification"
        verbose_name_plural = "Company Certifications"
    
    def __str__(self):
        return f"{self.certification_name} - {self.buyer.company_name}"
    
    def is_valid(self):
        """Check if the certification is still valid based on expiry date"""
        if not self.expiry_date:
            return True
        return self.expiry_date >= timezone.now().date()


class FarmerToBuyerReview(models.Model):
    """
    Model for farmers to review buyers
    """
    farmer = models.ForeignKey('FarmerProfile', on_delete=models.CASCADE, related_name='reviews_given')
    buyer = models.ForeignKey('BuyerProfile', on_delete=models.CASCADE, related_name='reviews_received')
    product = models.ForeignKey('FarmerProduct', on_delete=models.SET_NULL, null=True, blank=True, related_name='farmer_reviews')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Quantity of product")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Price of transaction in USD")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5 stars"
    )
    content = models.TextField(help_text="Review content")
    review_image = models.ImageField(upload_to='review_images/', null=True, blank=True, help_text="Optional image for the review")
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Farmer to Buyer Review"
        verbose_name_plural = "Farmer to Buyer Reviews"
    
    def __str__(self):
        return f"{self.farmer.first_name} {self.farmer.last_name}'s review of {self.buyer.company_name}"

class BuyerToFarmerReview(models.Model):
    """
    Model for buyers to review farmers
    """
    buyer = models.ForeignKey('BuyerProfile', on_delete=models.CASCADE, related_name='reviews_given')
    farmer = models.ForeignKey('FarmerProfile', on_delete=models.CASCADE, related_name='reviews_received')
    product = models.ForeignKey('FarmerProduct', on_delete=models.SET_NULL, null=True, blank=True, related_name='buyer_reviews')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Quantity of product")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Price of transaction in USD")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5 stars"
    )
    content = models.TextField(help_text="Review content")
    review_image = models.ImageField(upload_to='review_images/', null=True, blank=True, help_text="Optional image for the review")
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Buyer to Farmer Review"
        verbose_name_plural = "Buyer to Farmer Reviews"
    
    def __str__(self):
        return f"{self.buyer.company_name}'s review of {self.farmer.first_name} {self.farmer.last_name}"


from django.db import models
from django.utils import timezone

class FarmerCommunity(models.Model):
    """Farmer Community model"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    creator = models.ForeignKey('FarmerProfile', on_delete=models.CASCADE, related_name='created_communities')
    created_at = models.DateTimeField(default=timezone.now)
    
    # Additional fields
    cover_image = models.ImageField(upload_to='community_covers/', null=True, blank=True)
    location = models.CharField(max_length=200, blank=True)
    focus_products = models.ManyToManyField('ProductCategory', blank=True, related_name='communities')
    is_public = models.BooleanField(default=True)
    max_members = models.PositiveIntegerField(default=50)
    contact_email = models.EmailField(blank=True)
    
    class Meta:
        verbose_name = "Farmer Community"
        verbose_name_plural = "Farmer Communities"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def member_count(self):
        """Get the number of community members"""
        return self.members.count()
    
    @property
    def is_full(self):
        """Check if the community is full"""
        return self.member_count >= self.max_members


class CommunityMember(models.Model):
    """Community Member model"""
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('member', 'Member')
    ]
    
    community = models.ForeignKey(FarmerCommunity, on_delete=models.CASCADE, related_name='members')
    farmer = models.ForeignKey('FarmerProfile', on_delete=models.CASCADE, related_name='communities')
    joined_at = models.DateTimeField(default=timezone.now)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    
    class Meta:
        verbose_name = "Community Member"
        verbose_name_plural = "Community Members"
        unique_together = ('community', 'farmer')
    
    def __str__(self):
        return f"{self.farmer} - {self.community} ({self.get_role_display()})"
    

class LogisticCompany(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='logistic_company')
    company_name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='logistic_logos/', null=True, blank=True)
    bio = models.TextField(blank=True, help_text="Brief introduction about your logistics company")
    date_joined = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.company_name