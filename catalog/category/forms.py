'''Categories Forms'''

#Django
from django import forms
#App
from catalog.models import Category

class CategoryForm(forms.ModelForm):
    '''Formulario y validacion de categary'''
    name= forms.CharField(min_length=4,max_length=110)
    def clean(self):
        cleaned_data = super(CategoryForm,self).clean()
        return cleaned_data
    class Meta:
        model= Category
        fields = ['name','image']