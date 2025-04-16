from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .forms import CommunityEditForm, FarmerRegistrationForm
from .forms import BuyerRegistrationForm
from .models import FarmerProfile, BuyerProfile
from .models import FarmerProfile, Farm, FarmPhoto, FarmerProduct
from .models import BuyerProfile, ProductNeed
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .forms import ProfilePictureForm, CompanyLogoForm, FarmerProfileEditForm, FarmPhotoForm, FarmForm, FarmerProductForm, ProductNeedForm
from .forms import FarmerCertificationForm, LogisticCompanyLogoForm
from .forms import BuyerProfileEditForm, LogisticCompanyRegistrationForm
from .models import FarmerCertification, LogisticCompany
from .forms import CompanyCertificationForm, LogisticCompanyProfileEditForm
from .models import CompanyCertification
from .models import FarmerProfile, Farm, FarmPhoto, FarmerProduct, ProductCategory, ShippingMethod
from .models import BuyerProfile, ProductNeed, BuyerToFarmerReview, BuyerInterest, FarmerToBuyerReview
from .models import CommunityMember, FarmerCommunity
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.db.models import Q


def home(request):
    """
    Homepage view for the supplychain app
    """
    return render(request, 'supplychain/home.html', {
        'title': _('TropiConnect Home page')
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
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            try:
                farmer = FarmerProfile.objects.get(user=user)
                login(request, user)
                return redirect('farmer_dashboard') 
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
    try:
        farmer = FarmerProfile.objects.get(user=request.user)
    except FarmerProfile.DoesNotExist:
        raise PermissionDenied("You do not have access to this page.")
    
    farms = Farm.objects.filter(farmer=farmer)
    
    farm_data = []
    for farm in farms:
        photos = FarmPhoto.objects.filter(farm=farm)
        farm_data.append({
            'farm': farm,
            'photos': photos
        })
    
    products = FarmerProduct.objects.filter(farmer=farmer)
    
    buyer_reviews = BuyerToFarmerReview.objects.filter(farmer=farmer).order_by('-created_at')[:6]
    
    # Get communities the farmer is a member of
    communities = CommunityMember.objects.filter(farmer=farmer).select_related('community')
    
    # Get communities created by the farmer
    created_communities = FarmerCommunity.objects.filter(creator=farmer)
    
    context = {
        'title': 'Farmer Dashboard',
        'farmer': farmer,
        'farm_data': farm_data,
        'products': products,
        'buyer_reviews': buyer_reviews,
        'communities': communities,
        'created_communities': created_communities,
    }
    
    return render(request, 'supplychain/farmer_dashboard.html', context)

@login_required
def buyer_dashboard(request):
    try:
        buyer = BuyerProfile.objects.get(user=request.user)
    except BuyerProfile.DoesNotExist:
        raise PermissionDenied("You do not have access to this page.")
    
    product_needs = ProductNeed.objects.filter(buyer=buyer)
    
    farmer_reviews = FarmerToBuyerReview.objects.filter(buyer=buyer).order_by('-created_at')[:6]
    
    context = {
        'title': 'Buyer Dashboard',
        'buyer': buyer,
        'product_needs': product_needs,
        'farmer_reviews': farmer_reviews,  # 添加到上下文中
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


@login_required
def update_company_logo(request):
    """View for updating the buyer's company logo."""
    try:
        buyer = BuyerProfile.objects.get(user=request.user)
    except BuyerProfile.DoesNotExist:
        raise PermissionDenied("You do not have access to this page.")
    
    if request.method == 'POST':
        form = CompanyLogoForm(request.POST, request.FILES, instance=buyer)
        if form.is_valid():
            form.save()
            return redirect('buyer_dashboard')
    else:
        form = CompanyLogoForm(instance=buyer)
    
    context = {
        'title': 'Update Company Logo',
        'form': form,
        'buyer': buyer
    }
    
    return render(request, 'supplychain/update_company_logo.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def edit_farmer_profile(request):
    """View for editing farmer's profile information."""
    try:
        farmer = FarmerProfile.objects.get(user=request.user)
    except FarmerProfile.DoesNotExist:
        raise PermissionDenied("You do not have access to this page.")
    
    if request.method == 'POST':
        form = FarmerProfileEditForm(request.POST, instance=farmer)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('farmer_dashboard')
    else:
        form = FarmerProfileEditForm(instance=farmer)
    
    context = {
        'title': 'Edit Profile',
        'form': form,
        'farmer': farmer
    }
    
    return render(request, 'supplychain/edit_farmer_profile.html', context)


@login_required
def add_farm_photo(request, farm_id):
    """View for adding photos to a farm."""
    try:
        farmer = FarmerProfile.objects.get(user=request.user)
        farm = Farm.objects.get(id=farm_id, farmer=farmer)
    except (FarmerProfile.DoesNotExist, Farm.DoesNotExist):
        raise PermissionDenied("You do not have access to this farm.")
    
    photo_count = FarmPhoto.objects.filter(farm=farm).count()
    
    if request.method == 'POST':
        form = FarmPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            if photo_count >= 3:
                messages.error(request, "You can only have a maximum of 3 photos per farm. Please delete some photos first.")
            else:
                photo = form.save(commit=False)
                photo.farm = farm
                photo.save()
                messages.success(request, "Photo added successfully!")
            return redirect('farmer_dashboard')
    else:
        form = FarmPhotoForm()
    
    context = {
        'title': f'Add Photo to {farm.farm_name}',
        'form': form,
        'farm': farm,
        'photo_count': photo_count,
        'photos': FarmPhoto.objects.filter(farm=farm)
    }
    
    return render(request, 'supplychain/add_farm_photo.html', context)

@login_required
def delete_farm_photo(request, photo_id):
    """View for deleting a farm photo."""
    try:
        farmer = FarmerProfile.objects.get(user=request.user)
        photo = FarmPhoto.objects.get(id=photo_id, farm__farmer=farmer)
    except (FarmerProfile.DoesNotExist, FarmPhoto.DoesNotExist):
        raise PermissionDenied("You do not have access to this photo.")
    
    if request.method == 'POST':
        photo.delete()
        messages.success(request, "Photo deleted successfully!")
    
    return redirect('farmer_dashboard')


@login_required
def add_farm(request):
    """View for adding a new farm."""
    try:
        farmer = FarmerProfile.objects.get(user=request.user)
    except FarmerProfile.DoesNotExist:
        raise PermissionDenied("You do not have access to this page.")
    
    if request.method == 'POST':
        form = FarmForm(request.POST)
        if form.is_valid():
            farm = form.save(commit=False)
            farm.farmer = farmer
            farm.save()
            messages.success(request, "Farm added successfully!")
            return redirect('farmer_dashboard')
    else:
        form = FarmForm()
    
    context = {
        'title': 'Add New Farm',
        'form': form
    }
    
    return render(request, 'supplychain/add_farm.html', context)

@login_required
def add_product(request):
    """View for adding a new product."""
    try:
        farmer = FarmerProfile.objects.get(user=request.user)
    except FarmerProfile.DoesNotExist:
        raise PermissionDenied("You do not have access to this page.")
    
    if request.method == 'POST':
        form = FarmerProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.farmer = farmer
            product.save()
            messages.success(request, "Product added successfully!")
            return redirect('farmer_dashboard')
    else:
        form = FarmerProductForm()
    
    categories = ProductCategory.objects.all()
    
    context = {
        'title': 'Add New Product',
        'form': form,
        'categories': categories
    }
    
    return render(request, 'supplychain/add_product.html', context)


@login_required
def delete_product(request, product_id):
    """View for deleting a product."""
    try:
        farmer = FarmerProfile.objects.get(user=request.user)
        product = FarmerProduct.objects.get(id=product_id, farmer=farmer)
    except (FarmerProfile.DoesNotExist, FarmerProduct.DoesNotExist):
        raise PermissionDenied("You do not have access to this product.")
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, "Product deleted successfully!")
    
    return redirect('farmer_dashboard')


@login_required
def edit_product(request, product_id):
    """View for editing an existing product."""
    try:
        farmer = FarmerProfile.objects.get(user=request.user)
        product = FarmerProduct.objects.get(id=product_id, farmer=farmer)
    except (FarmerProfile.DoesNotExist, FarmerProduct.DoesNotExist):
        raise PermissionDenied("You do not have access to this product.")
    
    if request.method == 'POST':
        form = FarmerProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect('farmer_dashboard')
    else:
        form = FarmerProductForm(instance=product)
    
    context = {
        'title': 'Edit Product',
        'form': form,
        'product': product
    }
    
    return render(request, 'supplychain/edit_product.html', context)



@login_required
def farmer_home_page(request):
    """Home page for farmers. Only accessible to users with a farmer profile."""
    try:
        # Check if the logged-in user has a farmer profile
        farmer = FarmerProfile.objects.get(user=request.user)
    except FarmerProfile.DoesNotExist:
        # If no farmer profile exists for this user, redirect them to a generic page
        messages.error(request, "You need a farmer account to access this page.")
        return redirect('home')
    
    product_categories = ProductCategory.objects.all()
    
    selected_category = request.GET.get('category', '')
    is_random = request.GET.get('random', '') == 'true'
    
    if selected_category:
        try:
            category = ProductCategory.objects.get(id=selected_category)
            all_needs = ProductNeed.objects.filter(
                product_category=category,
                status='active'
            )
            
            if is_random and all_needs.count() > 3:
                import random
                need_ids = list(all_needs.values_list('id', flat=True))
                random_ids = random.sample(need_ids, min(3, len(need_ids)))
                product_needs = ProductNeed.objects.filter(id__in=random_ids)
            else:
                product_needs = all_needs.order_by('-date_posted')[:3]
        except ProductCategory.DoesNotExist:
            product_needs = []
    else:
        all_needs = ProductNeed.objects.filter(status='active')
        
        if is_random and all_needs.count() > 3:
            import random
            need_ids = list(all_needs.values_list('id', flat=True))
            random_ids = random.sample(need_ids, min(3, len(need_ids)))
            product_needs = ProductNeed.objects.filter(id__in=random_ids)
        else:
            product_needs = all_needs.order_by('-date_posted')[:3]
    is_random_logistic = request.GET.get('random_logistic', '') == 'true'
    
    all_logistics = LogisticCompany.objects.all()
    
    if is_random_logistic and all_logistics.count() > 3:
        import random
        logistic_ids = list(all_logistics.values_list('id', flat=True))
        random_ids = random.sample(logistic_ids, min(3, len(logistic_ids)))
        logistic_companies = LogisticCompany.objects.filter(id__in=random_ids)
    else:
        logistic_companies = all_logistics.order_by('?')[:3]

    context = {
        'title': 'Farmer Home',
        'farmer': farmer,
        'product_categories': product_categories,
        'selected_category': selected_category,
        'product_needs': product_needs,
        'is_random': is_random,
        'logistic_companies': logistic_companies,
        'is_random_logistic': is_random_logistic
    }
    
    return render(request, 'supplychain/farmer_home_page.html', context)


@login_required
def farmer_add_certification(request):
    """View for adding a new certification."""
    try:
        farmer = FarmerProfile.objects.get(user=request.user)
    except FarmerProfile.DoesNotExist:
        raise PermissionDenied("You do not have access to this page.")
    
    if request.method == 'POST':
        form = FarmerCertificationForm(request.POST, request.FILES)
        if form.is_valid():
            certification = form.save(commit=False)
            certification.farmer = farmer
            certification.save()
            messages.success(request, "Certification added successfully!")
            return redirect('farmer_dashboard')
    else:
        form = FarmerCertificationForm()
    
    context = {
        'title': 'Add New Certification',
        'form': form
    }
    
    return render(request, 'supplychain/farmer_add_certification.html', context)

@login_required
def farmer_edit_certification(request, certification_id):
    """View for editing an existing certification."""
    try:
        farmer = FarmerProfile.objects.get(user=request.user)
        certification = FarmerCertification.objects.get(id=certification_id, farmer=farmer)
    except (FarmerProfile.DoesNotExist, FarmerCertification.DoesNotExist):
        raise PermissionDenied("You do not have access to this certification.")
    
    if request.method == 'POST':
        form = FarmerCertificationForm(request.POST, request.FILES, instance=certification)
        if form.is_valid():
            form.save()
            messages.success(request, "Certification updated successfully!")
            return redirect('farmer_dashboard')
    else:
        form = FarmerCertificationForm(instance=certification)
    
    context = {
        'title': 'Edit Certification',
        'form': form,
        'certification': certification
    }
    
    return render(request, 'supplychain/farmer_edit_certification.html', context)

@login_required
def farmer_delete_certification(request, certification_id):
    """View for deleting a certification."""
    try:
        farmer = FarmerProfile.objects.get(user=request.user)
        certification = FarmerCertification.objects.get(id=certification_id, farmer=farmer)
    except (FarmerProfile.DoesNotExist, FarmerCertification.DoesNotExist):
        raise PermissionDenied("You do not have access to this certification.")
    
    if request.method == 'POST':
        certification.delete()
        messages.success(request, "Certification deleted successfully!")
    
    return redirect('farmer_dashboard')


@login_required
def edit_buyer_profile(request):
    """View for editing buyer's profile information."""
    try:
        buyer = BuyerProfile.objects.get(user=request.user)
    except BuyerProfile.DoesNotExist:
        raise PermissionDenied("You do not have access to this page.")
    
    if request.method == 'POST':
        form = BuyerProfileEditForm(request.POST, instance=buyer)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('buyer_dashboard')
    else:
        form = BuyerProfileEditForm(instance=buyer)
    
    context = {
        'title': 'Edit Company Profile',
        'form': form,
        'buyer': buyer
    }
    
    return render(request, 'supplychain/edit_buyer_profile.html', context)

@login_required
def add_product_need(request):
    """View for adding a new product need."""
    try:
        buyer = BuyerProfile.objects.get(user=request.user)
    except BuyerProfile.DoesNotExist:
        raise PermissionDenied("You do not have access to this page.")
    
    if request.method == 'POST':
        form = ProductNeedForm(request.POST)
        if form.is_valid():
            product_need = form.save(commit=False)
            product_need.buyer = buyer
            product_need.status = 'active'
            product_need.save()
            messages.success(request, "Product need added successfully!")
            return redirect('buyer_dashboard')
    else:
        form = ProductNeedForm()
    
    categories = ProductCategory.objects.all()
    
    context = {
        'title': 'Add New Product Need',
        'form': form,
        'categories': categories
    }
    
    return render(request, 'supplychain/add_product_need.html', context)

@login_required
def edit_product_need(request, need_id):
    """View for editing an existing product need."""
    try:
        buyer = BuyerProfile.objects.get(user=request.user)
        product_need = ProductNeed.objects.get(id=need_id, buyer=buyer)
    except (BuyerProfile.DoesNotExist, ProductNeed.DoesNotExist):
        raise PermissionDenied("You do not have access to this product need.")
    
    if request.method == 'POST':
        form = ProductNeedForm(request.POST, instance=product_need)
        if form.is_valid():
            form.save()
            messages.success(request, "Product need updated successfully!")
            return redirect('buyer_dashboard')
    else:
        form = ProductNeedForm(instance=product_need)
    
    context = {
        'title': 'Edit Product Need',
        'form': form,
        'product_need': product_need
    }
    
    return render(request, 'supplychain/edit_product_need.html', context)

@login_required
def delete_product_need(request, need_id):
    """View for deleting a product need."""
    try:
        buyer = BuyerProfile.objects.get(user=request.user)
        product_need = ProductNeed.objects.get(id=need_id, buyer=buyer)
    except (BuyerProfile.DoesNotExist, ProductNeed.DoesNotExist):
        raise PermissionDenied("You do not have access to this product need.")
    
    if request.method == 'POST':
        product_need.delete()
        messages.success(request, "Product need deleted successfully!")
    
    return redirect('buyer_dashboard')

@login_required
def update_product_need_status(request, need_id):
    """View for updating the status of a product need."""
    try:
        buyer = BuyerProfile.objects.get(user=request.user)
        product_need = ProductNeed.objects.get(id=need_id, buyer=buyer)
    except (BuyerProfile.DoesNotExist, ProductNeed.DoesNotExist):
        raise PermissionDenied("You do not have access to this product need.")
    
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in [choice[0] for choice in ProductNeed.STATUS_CHOICES]:
            product_need.status = status
            product_need.save()
            messages.success(request, f"Product need status updated to {dict(ProductNeed.STATUS_CHOICES)[status]}!")
        else:
            messages.error(request, "Invalid status selected.")
    
    return redirect('buyer_dashboard')

@login_required
def add_company_certification(request):
    """View for adding a new company certification."""
    try:
        buyer = BuyerProfile.objects.get(user=request.user)
    except BuyerProfile.DoesNotExist:
        raise PermissionDenied("You do not have access to this page.")
    
    if request.method == 'POST':
        form = CompanyCertificationForm(request.POST, request.FILES)
        if form.is_valid():
            certification = form.save(commit=False)
            certification.buyer = buyer
            certification.save()
            messages.success(request, "Certification added successfully!")
            return redirect('buyer_dashboard')
    else:
        form = CompanyCertificationForm()
    
    context = {
        'title': 'Add New Company Certification',
        'form': form
    }
    
    return render(request, 'supplychain/add_company_certification.html', context)

@login_required
def edit_company_certification(request, certification_id):
    """View for editing an existing company certification."""
    try:
        buyer = BuyerProfile.objects.get(user=request.user)
        certification = CompanyCertification.objects.get(id=certification_id, buyer=buyer)
    except (BuyerProfile.DoesNotExist, CompanyCertification.DoesNotExist):
        raise PermissionDenied("You do not have access to this certification.")
    
    if request.method == 'POST':
        form = CompanyCertificationForm(request.POST, request.FILES, instance=certification)
        if form.is_valid():
            form.save()
            messages.success(request, "Certification updated successfully!")
            return redirect('buyer_dashboard')
    else:
        form = CompanyCertificationForm(instance=certification)
    
    context = {
        'title': 'Edit Company Certification',
        'form': form,
        'certification': certification
    }
    
    return render(request, 'supplychain/edit_company_certification.html', context)

@login_required
def delete_company_certification(request, certification_id):
    """View for deleting a company certification."""
    try:
        buyer = BuyerProfile.objects.get(user=request.user)
        certification = CompanyCertification.objects.get(id=certification_id, buyer=buyer)
    except (BuyerProfile.DoesNotExist, CompanyCertification.DoesNotExist):
        raise PermissionDenied("You do not have access to this certification.")
    
    if request.method == 'POST':
        certification.delete()
        messages.success(request, "Certification deleted successfully!")
    
    return redirect('buyer_dashboard')

@login_required
def buyer_home_page(request):
    """Home page for buyers. Only accessible to users with a buyer profile."""
    try:
        # Check if the logged-in user has a buyer profile
        buyer = BuyerProfile.objects.get(user=request.user)
    except BuyerProfile.DoesNotExist:
        # If no buyer profile exists for this user, redirect them to a generic page
        messages.error(request, "You need a buyer account to access this page.")
        return redirect('home')
    
    product_categories = ProductCategory.objects.all()

    selected_category = request.GET.get('category', '')
    is_random = request.GET.get('random', '') == 'true'
    
    if selected_category:
        try:
            category = ProductCategory.objects.get(id=selected_category)
            all_products = FarmerProduct.objects.filter(
                category=category,
                is_available=True
            )
            
            if is_random and all_products.count() > 3:
                import random
                product_ids = list(all_products.values_list('id', flat=True))
                random_ids = random.sample(product_ids, min(3, len(product_ids)))
                farmer_products = FarmerProduct.objects.filter(id__in=random_ids)
            else:
                farmer_products = all_products[:3]
        except ProductCategory.DoesNotExist:
            farmer_products = []
    else:
        all_products = FarmerProduct.objects.filter(is_available=True)
        
        if is_random and all_products.count() > 3:
            import random
            product_ids = list(all_products.values_list('id', flat=True))
            random_ids = random.sample(product_ids, min(3, len(product_ids)))
            farmer_products = FarmerProduct.objects.filter(id__in=random_ids)
        else:
            farmer_products = all_products[:3]
    
    context = {
        'title': 'Buyer Home',
        'buyer': buyer,
        'product_categories': product_categories,
        'selected_category': selected_category,
        'farmer_products': farmer_products,
        'is_random': is_random
    }
    
    return render(request, 'supplychain/buyer_home_page.html', context)


@login_required
def view_farmer_profile(request, farmer_id):
    """View for buyers to see a farmer's profile."""
    try:
        buyer = BuyerProfile.objects.get(user=request.user)
        farmer = FarmerProfile.objects.get(id=farmer_id)
    except BuyerProfile.DoesNotExist:
        messages.error(request, "You need a buyer account to access this page.")
        return redirect('home')
    except FarmerProfile.DoesNotExist:
        messages.error(request, "Farmer not found.")
        return redirect('buyer_home')
    
    farms = Farm.objects.filter(farmer=farmer)
    
    products = FarmerProduct.objects.filter(farmer=farmer, is_available=True)
    
    certifications = FarmerCertification.objects.filter(farmer=farmer)
    
    buyer_reviews = BuyerToFarmerReview.objects.filter(farmer=farmer).order_by('-created_at')[:6]
    
    farm_data = []
    for farm in farms:
        photos = FarmPhoto.objects.filter(farm=farm)
        farm_data.append({
            'farm': farm,
            'photos': photos
        })
    
    context = {
        'title': f'{farmer.first_name} {farmer.last_name}\'s Profile',
        'farmer': farmer,
        'farm_data': farm_data,
        'products': products,
        'certifications': certifications,
        'buyer_reviews': buyer_reviews,
    }
    
    return render(request, 'supplychain/view_farmer_profile.html', context)


@login_required
def view_buyer_profile(request, buyer_id):
    """View for farmers to see a buyer's profile."""
    try:
        farmer = FarmerProfile.objects.get(user=request.user)
        buyer = BuyerProfile.objects.get(id=buyer_id)
    except FarmerProfile.DoesNotExist:
        messages.error(request, "You need a farmer account to access this page.")
        return redirect('home')
    except BuyerProfile.DoesNotExist:
        messages.error(request, "Buyer not found.")
        return redirect('farmer_home')
    
    product_needs = ProductNeed.objects.filter(buyer=buyer, status='active').order_by('-date_posted')
    
    farmer_reviews = FarmerToBuyerReview.objects.filter(buyer=buyer).order_by('-created_at')[:6]
    
    my_products = FarmerProduct.objects.filter(farmer=farmer)
    
    context = {
        'title': f'{buyer.company_name} Profile',
        'buyer': buyer,
        'product_needs': product_needs,
        'farmer_reviews': farmer_reviews,
        'my_products': my_products,
    }
    
    return render(request, 'supplychain/view_buyer_profile.html', context)

@login_required
def leave_farmer_review(request, farmer_id):
    """View for buyers to leave a review for a farmer."""
    try:
        buyer = BuyerProfile.objects.get(user=request.user)
        farmer = FarmerProfile.objects.get(id=farmer_id)
    except BuyerProfile.DoesNotExist:
        messages.error(request, "You need a buyer account to leave a review.")
        return redirect('home')
    except FarmerProfile.DoesNotExist:
        messages.error(request, "Farmer not found.")
        return redirect('buyer_home')
    
    if request.method == 'POST':
        product_id = request.POST.get('product')
        product = None
        if product_id:
            try:
                product = FarmerProduct.objects.get(id=product_id)
            except FarmerProduct.DoesNotExist:
                pass
        
        rating = request.POST.get('rating')
        content = request.POST.get('content')
        quantity = request.POST.get('quantity') or None
        price = request.POST.get('price') or None
        
        review = BuyerToFarmerReview(
            buyer=buyer,
            farmer=farmer,
            rating=rating,
            content=content,
            product=product
        )
        
        if quantity:
            review.quantity = quantity
        if price:
            review.price = price
        
        if 'review_image' in request.FILES:
            review.review_image = request.FILES['review_image']
        
        review.save()
        messages.success(request, "Your review has been submitted successfully!")
        
    return redirect('view_farmer_profile', farmer_id=farmer_id)


@login_required
def leave_buyer_review(request, buyer_id):
    """View for farmers to leave a review for a buyer."""
    try:
        farmer = FarmerProfile.objects.get(user=request.user)
        buyer = BuyerProfile.objects.get(id=buyer_id)
    except FarmerProfile.DoesNotExist:
        messages.error(request, "You need a farmer account to leave a review.")
        return redirect('home')
    except BuyerProfile.DoesNotExist:
        messages.error(request, "Buyer not found.")
        return redirect('farmer_home')
    
    if request.method == 'POST':
        product_id = request.POST.get('product')
        product = None
        if product_id:
            try:
                product = FarmerProduct.objects.get(id=product_id, farmer=farmer)
            except FarmerProduct.DoesNotExist:
                pass
        
        rating = request.POST.get('rating')
        content = request.POST.get('content')
        quantity = request.POST.get('quantity') or None
        price = request.POST.get('price') or None
        
        review = FarmerToBuyerReview(
            farmer=farmer,
            buyer=buyer,
            rating=rating,
            content=content,
            product=product
        )
        
        if quantity:
            review.quantity = quantity
        if price:
            review.price = price
        
        if 'review_image' in request.FILES:
            review.review_image = request.FILES['review_image']
        
        review.save()
        messages.success(request, "Your review has been submitted successfully!")
        
    return redirect('view_buyer_profile', buyer_id=buyer_id)

@login_required
def create_community(request):
    """Create a new farmer community"""
    try:
        farmer = FarmerProfile.objects.get(user=request.user)
    except FarmerProfile.DoesNotExist:
        messages.error(request, "Only farmers can create communities")
        return redirect('home')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        location = request.POST.get('location', '')
        
        if not name or not description:
            messages.error(request, "Community name and description are required")
            return redirect('create_community')
        
        # Create the community
        community = FarmerCommunity.objects.create(
            name=name,
            description=description,
            creator=farmer,
            location=location
        )
        
        # Add creator as a member with admin role
        CommunityMember.objects.create(
            community=community,
            farmer=farmer,
            role='admin'
        )
        
        messages.success(request, f"Community '{name}' created successfully!")
        return redirect('farmer_dashboard')
        
    return render(request, 'supplychain/create_community.html', {
        'title': 'Create Community'
    })

@login_required
def community_detail(request, community_id):
    """View community details"""
    try:
        farmer = FarmerProfile.objects.get(user=request.user)
    except FarmerProfile.DoesNotExist:
        messages.error(request, "Only farmers can view community details")
        return redirect('home')
    
    community = get_object_or_404(FarmerCommunity, id=community_id)
    
    # Check if user is a member
    is_member = CommunityMember.objects.filter(community=community, farmer=farmer).exists()
    
    # Get member role if applicable
    user_role = None
    if is_member:
        membership = CommunityMember.objects.get(community=community, farmer=farmer)
        user_role = membership.role
    
    # Get all members
    members = CommunityMember.objects.filter(community=community).select_related('farmer')
    
    context = {
        'title': community.name,
        'community': community,
        'is_member': is_member,
        'user_role': user_role,
        'members': members,
        'farmer': farmer
    }
    
    return render(request, 'supplychain/community_detail.html', context)

@login_required
def join_community(request, community_id):
    """Join a community"""
    try:
        farmer = FarmerProfile.objects.get(user=request.user)
    except FarmerProfile.DoesNotExist:
        messages.error(request, "Only farmers can join communities")
        return redirect('home')
    
    community = get_object_or_404(FarmerCommunity, id=community_id)
    
    # Check if already a member
    if CommunityMember.objects.filter(community=community, farmer=farmer).exists():
        messages.info(request, "You are already a member of this community")
        return redirect('community_detail', community_id=community.id)
    
    # Check if community is full
    if community.is_full:
        messages.error(request, "This community has reached its maximum capacity")
        return redirect('community_detail', community_id=community.id)
    
    # Add as member
    CommunityMember.objects.create(
        community=community,
        farmer=farmer,
        role='member'
    )
    
    messages.success(request, f"You have successfully joined the '{community.name}' community!")
    return redirect('community_detail', community_id=community.id)

@login_required
def leave_community(request, community_id):
    """Leave a community"""
    try:
        farmer = FarmerProfile.objects.get(user=request.user)
    except FarmerProfile.DoesNotExist:
        messages.error(request, "Only farmers can leave communities")
        return redirect('home')
    
    community = get_object_or_404(FarmerCommunity, id=community_id)
    
    # Check if user is a member
    try:
        membership = CommunityMember.objects.get(community=community, farmer=farmer)
        
        # Creator cannot leave
        if community.creator == farmer:
            messages.error(request, "As the creator, you cannot leave the community")
            return redirect('community_detail', community_id=community.id)
        
        # Delete membership
        membership.delete()
        messages.success(request, f"You have left the '{community.name}' community")
        
    except CommunityMember.DoesNotExist:
        messages.error(request, "You are not a member of this community")
    
    return redirect('farmer_dashboard')

@login_required
def browse_communities(request):
    """View for browsing available communities"""
    try:
        farmer = FarmerProfile.objects.get(user=request.user)
    except FarmerProfile.DoesNotExist:
        messages.error(request, "Only farmers can browse communities")
        return redirect('home')
    
    # Get search query
    query = request.GET.get('query', '')
    
    # Get all public communities
    communities = FarmerCommunity.objects.filter(is_public=True)
    
    # Apply search filter if query exists
    if query:
        communities = communities.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query)
        )
    
    # Get communities the farmer is already a member of
    joined_communities = CommunityMember.objects.filter(farmer=farmer).values_list('community_id', flat=True)
    
    context = {
        'title': 'Browse Communities',
        'communities': communities,
        'joined_communities': joined_communities,
        'query': query,
        'farmer': farmer
    }
    
    return render(request, 'supplychain/browse_communities.html', context)

@login_required
def edit_community(request, community_id):
    """Edit a community"""
    try:
        farmer = FarmerProfile.objects.get(user=request.user)
    except FarmerProfile.DoesNotExist:
        messages.error(request, "Only farmers can edit communities")
        return redirect('home')
    
    community = get_object_or_404(FarmerCommunity, id=community_id)
    
    # Check if user is creator or admin
    is_creator = community.creator == farmer
    try:
        membership = CommunityMember.objects.get(community=community, farmer=farmer)
        is_admin = membership.role == 'admin'
    except CommunityMember.DoesNotExist:
        is_admin = False
    
    if not (is_creator or is_admin):
        messages.error(request, "You don't have permission to edit this community")
        return redirect('community_detail', community_id=community.id)
    
    if request.method == 'POST':
        form = CommunityEditForm(request.POST, request.FILES, instance=community)
        if form.is_valid():
            form.save()
            messages.success(request, f"Community '{community.name}' has been updated successfully!")
            return redirect('community_detail', community_id=community.id)
    else:
        form = CommunityEditForm(instance=community)
    
    context = {
        'title': f'Edit {community.name}',
        'form': form,
        'community': community,
        'farmer': farmer,
        'is_creator': is_creator
    }
    
    return render(request, 'supplychain/edit_community.html', context)

def market_preparation_guides(request):
    """
    View to display international market preparation guides
    """
    return render(request, 'supplychain/market_preparation_guides.html')


def certification_help(request):
    return render(request, 'supplychain/certification_help.html', {'title': 'Certification Help'})

def register_logistic(request):
    if request.method == 'POST':
        form = LogisticCompanyRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = LogisticCompanyRegistrationForm()
    
    return render(request, 'supplychain/register_logistic.html', {
        'title': 'Logistics Company Registration',
        'form': form
    })

def logistic_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        company_name = request.POST.get('company_name')
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            try:
                logistic = LogisticCompany.objects.get(user=user)
                if logistic.company_name == company_name:
                    login(request, user)
                    return redirect('logistic_dashboard')  # 登录成功后重定向到物流公司仪表板页面
                else:
                    messages.error(request, "Company name doesn't match.")
            except LogisticCompany.DoesNotExist:
                messages.error(request, "Logistics company profile not found.")
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'supplychain/logistic_login.html', {'title': 'Logistics Company Login'})

@login_required
def logistic_dashboard(request):
    """Dashboard view for logistics companies."""
    try:
        logistic = LogisticCompany.objects.get(user=request.user)
    except LogisticCompany.DoesNotExist:
        raise PermissionDenied("You do not have access to this page.")
    
    context = {
        'title': 'Logistics Company Dashboard',
        'logistic': logistic,
    }
    
    return render(request, 'supplychain/logistic_dashboard.html', context)

@login_required
def update_logistic_logo(request):
    """View for updating the logistics company's logo."""
    try:
        logistic = LogisticCompany.objects.get(user=request.user)
    except LogisticCompany.DoesNotExist:
        raise PermissionDenied("You do not have access to this page.")
    
    if request.method == 'POST':
        form = LogisticCompanyLogoForm(request.POST, request.FILES, instance=logistic)
        if form.is_valid():
            form.save()
            messages.success(request, "Company logo updated successfully!")
            return redirect('logistic_dashboard')
    else:
        form = LogisticCompanyLogoForm(instance=logistic)
    
    context = {
        'title': 'Update Company Logo',
        'form': form,
        'logistic': logistic
    }
    
    return render(request, 'supplychain/update_logistic_logo.html', context)

@login_required
def edit_logistic_profile(request):
    """View for editing logistics company's profile information."""
    try:
        logistic = LogisticCompany.objects.get(user=request.user)
    except LogisticCompany.DoesNotExist:
        raise PermissionDenied("You do not have access to this page.")
    
    if request.method == 'POST':
        form = LogisticCompanyProfileEditForm(request.POST, instance=logistic)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('logistic_dashboard')
    else:
        form = LogisticCompanyProfileEditForm(instance=logistic)
    
    context = {
        'title': 'Edit Logistics Company Profile',
        'form': form,
        'logistic': logistic
    }
    
    return render(request, 'supplychain/edit_logistic_profile.html', context)

def view_logistic_profile(request, logistic_id):
    """View for seeing a logistics company's profile."""
    logistic = get_object_or_404(LogisticCompany, id=logistic_id)
    
    context = {
        'title': f'{logistic.company_name} Profile',
        'logistic': logistic,
    }
    
    return render(request, 'supplychain/view_logistic_profile.html', context)

@login_required
def order_history(request):
    """View for displaying a farmer's order history (demonstration only)."""
    try:
        farmer = FarmerProfile.objects.get(user=request.user)
    except FarmerProfile.DoesNotExist:
        raise PermissionDenied("You do not have access to this page.")
    
    
    context = {
        'title': 'Order History',
        'farmer': farmer,
    }
    
    return render(request, 'supplychain/order_history.html', context)


@login_required
def buyer_order_history(request):
    """View for displaying a buyer's order history (demonstration only)."""
    try:
        buyer = BuyerProfile.objects.get(user=request.user)
    except BuyerProfile.DoesNotExist:
        raise PermissionDenied("You do not have access to this page.")
    
    
    context = {
        'title': 'Purchase History',
        'buyer': buyer,
    }
    
    return render(request, 'supplychain/buyer_order_history.html', context)

def video_tutorials(request):
    """View for displaying video tutorials for farmers."""
    context = {
        'title': 'Video Tutorials',
    }
    return render(request, 'supplychain/video_tutorials.html', context)