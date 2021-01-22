from django import forms
from django.contrib.auth.models import User

#from locations.models import Country,Province,Canton
from orders.models import Client


class RegisterForm(forms.Form):
    firstname = forms.CharField(label='Nombre',widget=forms.TextInput(attrs={'class':'form-control'}))
    lastname = forms.CharField(label='Apellido',widget=forms.TextInput(attrs={'class':'form-control'}))
    username = forms.CharField(label='Nombre Usuario',widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label='Correo Electronico',widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='Contraseña',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    address= forms.CharField(label='Dirección Domiciliaria',widget=forms.TextInput(attrs={'class':'form-control'}))
    #country= forms.ModelChoiceField(queryset=Country.objects.all(),label='Pais', widget=forms.Select(attrs={'class':'form-control'}))
    #co= forms.CharField()
    #province= forms.ModelChoiceField(queryset=Province.objects.all(),label='Provincia', widget=forms.Select(attrs={'class':'form-control'}),required=True)
    #canton= forms.ModelChoiceField(queryset=Canton.objects.all(),label='Ciudad', widget=forms.Select(attrs={'class':'form-control'}),required=True)
    perfil = forms.ImageField(label='Image',widget=forms.FileInput(attrs={'class':'form-control'}))

