from django.contrib import admin
from .models import (
    FarmerProfile, Farm, FarmPhoto, ProductCategory, 
    FarmerProduct, ShippingMethod, FarmerShippingMethod,
    BuyerProfile, ProductNeed, BuyerInterest, FarmerToBuyerReview, BuyerToFarmerReview,
)

admin.site.register(FarmerProfile)
admin.site.register(Farm)
admin.site.register(FarmPhoto)
admin.site.register(ProductCategory)
admin.site.register(FarmerProduct)
admin.site.register(ShippingMethod)
admin.site.register(FarmerShippingMethod)
admin.site.register(BuyerProfile)
admin.site.register(ProductNeed)
admin.site.register(BuyerInterest)
admin.site.register(FarmerToBuyerReview)
admin.site.register(BuyerToFarmerReview)