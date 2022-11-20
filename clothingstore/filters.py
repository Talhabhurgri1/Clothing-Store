from django.forms import Widget
import django_filters
from .models import Product
from django import forms 

class ProductFilter(django_filters.FilterSet):
    #Categories
    categories = (
        ('shirt','shirt'),
        ('jeans','jeans'),
        ('shoes','shoes'),

    )
    #Size 
    size = (
        ('small','Small'),('medium','Medium'),('large','Large')
    )
    choices = ((900,'Under 900'),(1000,'Under 1000'),(2000,'Under 2000'))
     
    product_price = django_filters.ChoiceFilter(label="Price",choices=choices,widget=forms.Select(attrs={'class':'form-control'}))
    product_category = django_filters.ChoiceFilter(label="Category",choices=categories,widget=forms.Select(attrs={'class':'form-control'}))
    product_name = django_filters.CharFilter(label="Product",widget=forms.TextInput(attrs={'class':'form-control'}))
    product_size =django_filters.ChoiceFilter(label="Size",choices=size,widget=forms.Select(attrs={'class':'form-control'}))
    
    class Meta:
        model = Product 
        fields = {'product_category':['exact'],'product_price':['exact'],'product_size':['exact']}

    
