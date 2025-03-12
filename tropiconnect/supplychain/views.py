from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .forms import FarmerRegistrationForm
from .forms import BuyerRegistrationForm
from .models import FarmerProfile

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