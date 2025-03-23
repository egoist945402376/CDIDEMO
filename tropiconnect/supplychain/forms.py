from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import FarmerProfile
from .models import BuyerProfile
from .models import FarmPhoto
from .models import Farm
from .models import ProductNeed
from .models import FarmerProduct
from .models import FarmerCertification
import datetime
class FarmerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            FarmerProfile.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                phone_number=self.cleaned_data['phone_number']
            )
        return user

class BuyerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    company_name = forms.CharField(required=True)
    country = forms.CharField(required=True)
    city = forms.CharField(required=True)
    introduction = forms.CharField(widget=forms.Textarea, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super(BuyerRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Choose a username'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Your business email'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Create a password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm your password'})
        self.fields['company_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Your company name'})
        self.fields['country'].widget.attrs.update({'class': 'form-select'})
        self.fields['city'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Your city'})
        self.fields['introduction'].widget.attrs.update({
            'class': 'form-control', 
            'rows': '5', 
            'placeholder': 'Please introduce your company and describe what types of agricultural products you\'re interested in sourcing from Africa...'
        })
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            BuyerProfile.objects.create(
                user=user,
                company_name=self.cleaned_data['company_name'],
                country=self.cleaned_data['country'],
                city=self.cleaned_data['city'],
                introduction=self.cleaned_data['introduction']
            )
        return user


class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = FarmerProfile
        fields = ['profile_picture']
        widgets = {
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control', 
                'accept': 'image/*'
            })
        }


class CompanyLogoForm(forms.ModelForm):
    """Form used for updating company logo"""
    class Meta:
        model = BuyerProfile
        fields = ['company_logo']
        widgets = {
            'company_logo': forms.FileInput(attrs={
                'class': 'form-control', 
                'accept': 'image/*'
            })
        }


class FarmerProfileEditForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = FarmerProfile
        fields = ['phone_number', 'bio']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
    
    def __init__(self, *args, **kwargs):
        super(FarmerProfileEditForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['email'].initial = self.instance.user.email
    
    def save(self, commit=True):
        profile = super(FarmerProfileEditForm, self).save(commit=False)
        if commit:
            if profile.user:
                profile.user.email = self.cleaned_data['email']
                profile.user.save()
            profile.save()
        return profile

class FarmPhotoForm(forms.ModelForm):
    class Meta:
        model = FarmPhoto
        fields = ['photo', 'caption']
        widgets = {
            'photo': forms.FileInput(attrs={
                'class': 'form-control', 
                'accept': 'image/*'
            }),
            'caption': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Add a caption for this photo (optional)'
            })
        }


class FarmForm(forms.ModelForm):
    class Meta:
        model = Farm
        fields = ['farm_name', 'location', 'description', 'established_year']
        widgets = {
            'farm_name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'established_year': forms.NumberInput(attrs={'class': 'form-control'})
        }


class FarmerProductForm(forms.ModelForm):
    class Meta:
        model = FarmerProduct
        fields = ['product_name', 'category', 'description', 'is_available', 'photo']
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'photo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
        }


class FarmerCertificationForm(forms.ModelForm):
    class Meta:
        model = FarmerCertification
        fields = ['certification_name', 'issuing_organization', 'issue_date', 
                  'expiry_date', 'certificate_image', 'description']
        widgets = {
            'certification_name': forms.TextInput(attrs={'class': 'form-control'}),
            'issuing_organization': forms.TextInput(attrs={'class': 'form-control'}),
            'issue_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'certificate_image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class BuyerProfileEditForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = BuyerProfile
        fields = ['phone_number', 'company_name', 'country', 'city', 'introduction', 'website']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'introduction': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'website': forms.URLInput(attrs={'class': 'form-control'})
        }
    
    def __init__(self, *args, **kwargs):
        super(BuyerProfileEditForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['email'].initial = self.instance.user.email
    
    def save(self, commit=True):
        profile = super(BuyerProfileEditForm, self).save(commit=False)
        if commit:
            if profile.user:
                profile.user.email = self.cleaned_data['email']
                profile.user.save()
            profile.save()
        return profile

class ProductNeedForm(forms.ModelForm):
    class Meta:
        model = ProductNeed
        fields = ['product_name', 'product_category', 'description', 'quantity', 
                  'unit', 'price_per_kg', 'date_needed_by']
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control'}),
            'product_category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'unit': forms.Select(attrs={'class': 'form-control'}),
            'price_per_kg': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'date_needed_by': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        }
    
    def clean_date_needed_by(self):
        date_needed_by = self.cleaned_data.get('date_needed_by')
        if date_needed_by and date_needed_by < datetime.date.today():
            raise forms.ValidationError("The needed by date cannot be in the past.")
        return date_needed_by
    
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise forms.ValidationError("Quantity must be greater than zero.")
        return quantity
    
    def clean_price_per_kg(self):
        price = self.cleaned_data.get('price_per_kg')
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price





def __init__(self, *args, **kwargs):
    super(FarmerRegistrationForm, self).__init__(*args, **kwargs)
    self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
    self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'First Name'})
    self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Last Name'})
    self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email Address'})
    self.fields['phone_number'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Phone Number'})
    self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
    self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})