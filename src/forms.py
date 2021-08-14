'''
    People forms.py
    https://github.com/furious-luke/django-address
    https://docs.djangoproject.com/en/1.10/topics/forms/
'''
from .models import Person
from address.forms import AddressField
from django import forms
   
class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        address = AddressField()
        fields = '__all__'

