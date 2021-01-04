from django import forms
from .models import Stock
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ["ticker"]

class SignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control'}))
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
   
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class EditProfileForm(UserChangeForm):
    password = forms.CharField(widget=forms.TextInput(attrs={'type':'hidden '}))
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',  'email', 'password',)