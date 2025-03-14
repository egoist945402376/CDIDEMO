from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .forms import FarmerRegistrationForm
from .forms import BuyerRegistrationForm
from .models import FarmerProfile, BuyerProfile
from .models import FarmerProfile, Farm, FarmPhoto, FarmerProduct
from .models import BuyerProfile, ProductNeed
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .forms import ProfilePictureForm


def home(request):
    """
    Homepage view for the supplychain app
    """
    return render(request, 'supplychain/home.html', {
        'title': 'TropiConnect Homg page'
    })

def register_farmer(request):
    if request.method == 'POST':
        form = FarmerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect('home') 
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = FarmerRegistrationForm()
    
    return render(request, 'supplychain/register_farmer.html', {
        'title': 'Farmer Registration',
        'form': form
    })

def register_buyer(request):
    if request.method == 'POST':
        form = BuyerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful! You can now login.")
            return redirect('home')  
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = BuyerRegistrationForm()
    
    return render(request, 'supplychain/register_buyer.html', {
        'title': 'Buyer Registration',
        'form': form
    })


def farmer_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            try:
                farmer = FarmerProfile.objects.get(user=user)
                if farmer.first_name == first_name and farmer.last_name == last_name:
                    login(request, user)
                    return redirect('farmer_dashboard') 
                else:
                    messages.error(request, "First name or last name doesn't match.")
            except FarmerProfile.DoesNotExist:
                messages.error(request, "Farmer profile not found.")
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'supplychain/farmer_login.html', {'title': 'Farmer Login'})

def buyer_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        company_name = request.POST.get('company_name')
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            try:
                buyer = BuyerProfile.objects.get(user=user)
                if buyer.company_name == company_name:
                    login(request, user)
                    return redirect('buyer_dashboard') 
                else:
                    messages.error(request, "Company name doesn't match.")
            except BuyerProfile.DoesNotExist:
                messages.error(request, "Buyer profile not found.")
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'supplychain/buyer_login.html', {'title': 'Buyer Login'})


@login_required
def farmer_dashboard(request):
    """
    Dashboard view for farmers. Only accessible to users with a farmer profile.
    Displays personal information, farm details, and products.
    """
    try:
        # Try to get the farmer profile for the logged-in user
        farmer = FarmerProfile.objects.get(user=request.user)
    except FarmerProfile.DoesNotExist:
        # If no farmer profile exists for this user, they shouldn't access this page
        raise PermissionDenied("You do not have access to this page.")
    
    # Get the farms associated with this farmer
    farms = Farm.objects.filter(farmer=farmer)
    
    # Initialize a dictionary to store farms and their photos
    farm_data = []
    for farm in farms:
        photos = FarmPhoto.objects.filter(farm=farm)
        farm_data.append({
            'farm': farm,
            'photos': photos
        })
    
    # Get the products associated with this farmer
    products = FarmerProduct.objects.filter(farmer=farmer)
    
    context = {
        'title': 'Farmer Dashboard',
        'farmer': farmer,
        'farm_data': farm_data,
        'products': products,
    }
    
    return render(request, 'supplychain/farmer_dashboard.html', context)

@login_required
def buyer_dashboard(request):
    """
    Dashboard view for buyers. Only accessible to users with a buyer profile.
    Displays company information and product needs.
    """
    try:
        # Try to get the buyer profile for the logged-in user
        buyer = BuyerProfile.objects.get(user=request.user)
    except BuyerProfile.DoesNotExist:
        # If no buyer profile exists for this user, they shouldn't access this page
        raise PermissionDenied("You do not have access to this page.")
    
    # Get the product needs associated with this buyer
    product_needs = ProductNeed.objects.filter(buyer=buyer)
    
    context = {
        'title': 'Buyer Dashboard',
        'buyer': buyer,
        'product_needs': product_needs,
    }
    
    return render(request, 'supplychain/buyer_dashboard.html', context)


@login_required
def update_profile_picture(request):
    """View for updating the farmer's profile picture."""
    try:
        farmer = FarmerProfile.objects.get(user=request.user)
    except FarmerProfile.DoesNotExist:
        raise PermissionDenied("You do not have access to this page.")
    
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=farmer)
        if form.is_valid():
            form.save()
            return redirect('farmer_dashboard')
    else:
        form = ProfilePictureForm(instance=farmer)
    
    context = {
        'title': 'Update Profile Picture',
        'form': form,
        'farmer': farmer
    }
    
    return render(request, 'supplychain/update_profile_picture.html', context)