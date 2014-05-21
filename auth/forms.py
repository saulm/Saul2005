from django.contrib.auth.forms import UserCreationForm
from registration.forms import RegistrationFormTermsOfService
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import AuthenticationForm
from auth.utils import get_user_type
from auth.models import CustomerProfile, BusinessProfile

class AdminUserCreationForm(UserCreationForm):
    USER_TYPES = (("C", "Customer"), ("B", "Business"))
    user_type = forms.ChoiceField(choices=USER_TYPES, required=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['username'].required = False
        self.fields['username'].widget = forms.widgets.HiddenInput()
        
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email").lower().strip()
        user_type = cleaned_data.get("user_type").upper().strip()
        
        if email and user_type:
            username = "%s_%s" % (user_type, email)
            cleaned_data['username'] = username
            try:
                user = User.objects.get(username = username)
            except ObjectDoesNotExist:
                return cleaned_data
            raise forms.ValidationError("A User with that email already exists")
        

class UserRegistrationForm(RegistrationFormTermsOfService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['username'].required = False
        self.fields['username'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email").lower().strip()
        
        if email:
            user_type = get_user_type()
            username = "%s_%s" % (user_type, email)
            cleaned_data['username'] = username

            try:
                user = User.objects.get(username = username)
            except ObjectDoesNotExist:
                return cleaned_data
            raise forms.ValidationError("A User with that email already exists")
                                
        return cleaned_data

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.HiddenInput, required=False)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput) 

    def clean(self):
        email = self.cleaned_data.get("email").lower().strip()
        user_type = get_user_type()
        self.cleaned_data['username'] = "%s_%s" % (user_type, email) 
        return super().clean()
        
class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        exclude = ["user"]

class BusinessProfileForm(forms.ModelForm):
    class Meta:
        model = BusinessProfile
        exclude = ["user"]
    
PROFILE_FORM = BusinessProfileForm if get_user_type() == "B" else CustomerProfileForm
