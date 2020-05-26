from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import datetime
from django.forms import ModelForm
from .models import Company

class personform(UserCreationForm):
     first_name = forms.CharField()
     last_name=forms.CharField()
     email=forms.EmailField()

     
     class Meta:
     	model=User
     	fields=['first_name','last_name','username','email', 'password1', 'password2']


class companyform(forms.ModelForm):

	class Meta:
		model=Company
		fields=['symbol','cname','sector','revenue','market_capital','no_of_stocks']
 
