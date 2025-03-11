from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import FarmerProfile

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



def __init__(self, *args, **kwargs):
    super(FarmerRegistrationForm, self).__init__(*args, **kwargs)
    self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
    self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email Address'})
    self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'First Name'})
    self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Last Name'})
    self.fields['phone_number'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Phone Number'})
    self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
    self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})