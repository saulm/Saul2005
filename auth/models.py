from django.db import models
from django.contrib.auth.models import User
from auth.utils import get_user_type

class CustomerProfile(models.Model):
    GENDER_CHOICES = (('F', 'Female'),('M', 'Male'))

    user = models.OneToOneField(User, related_name="customer_profile")
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    
class BusinessProfile(models.Model):
    user = models.OneToOneField(User, related_name="business_profile")
    company_name =  models.CharField(max_length=60)


PROFILE_CLASS = BusinessProfile if get_user_type() == "B" else CustomerProfile
