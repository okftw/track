from django import forms
from . import models
from django.forms import ModelForm
from .models import UserProfile

class CreateEntry(forms.ModelForm):
    class Meta:
        model = models.Entries
        fields = ['Tracking','String_Value','Numerical_Value','Additional_Information']
        exclude =[
            'Numerical_Value'
        ]
        widgets = {
            'Tracking': forms.HiddenInput(),
        }
        labels = {
            "String_Value": "Food"
        }

class CreateWeight(forms.ModelForm):
    class Meta:
        model = models.Entries
        fields = ['Tracking','String_Value','Numerical_Value','Additional_Information']
        exclude =[
            'String_Value','Additional_Information'
        ]
        widgets = {
            'Tracking': forms.HiddenInput(),
        }
        labels = {
            "String_Value": "Weight"
        }

class CreateBm(forms.ModelForm):
    class Meta:
        model = models.Entries
        fields = ['Tracking','String_Value','Numerical_Value','Additional_Information']
        exclude =[
            'String_Value'
        ]
        widgets = {
            'Tracking': forms.HiddenInput(),
        }
        labels = {
            "String_Value": "Stool"
        }

class AddMedication(forms.ModelForm):
    class Meta:
        model = models.Entries
        fields = ['Tracking','String_Value','Numerical_Value','Additional_Information']
        exclude =[
            'Numerical_Value'
        ]
        widgets = {
            'Tracking': forms.HiddenInput(),
        }
        labels = {
            "String_Value": "Medication"
        }

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        weight_tracker = forms.BooleanField(initial=True)
        fields = ['age','weight','height','weight_tracker','bm_tracker','countdown_number']
