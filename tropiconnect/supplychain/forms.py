from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import FarmerProfile
from .models import BuyerProfile

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



def __init__(self, *args, **kwargs):
    super(FarmerRegistrationForm, self).__init__(*args, **kwargs)
    self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
    self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'First Name'})
    self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Last Name'})
    self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email Address'})
    self.fields['phone_number'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Phone Number'})
    self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
    self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})