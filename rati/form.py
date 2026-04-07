from django import forms
from .models import Profile,Product,Category

class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['profile_picture','bio','dob']
        

        widgets={
            'dob':forms.DateInput(attrs={'type':'date'})
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'image','location','categories']


class ProductSearchForm(forms.Form):
    title = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search products...'})
    )
    
    location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Location'})
    )
    
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    min_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'Min price'})
    )

    max_price = forms.DecimalField(  # ✅ You missed this one
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'Max price'})
    )
