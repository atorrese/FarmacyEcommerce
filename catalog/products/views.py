from itertools import product

from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView,View,ListView

from FarmacyEcommerce.funciones import DataUser
from cart.forms import  CartAddProductForm, CartAdd
from cart.models import Cart
from catalog.models import Product,Category
from utils.mixins import OldDataMixin

class Index(ListView, OldDataMixin):
    model = Product
    template_name ='index.html'
    paginate_by = 3
    context_object_name = 'products'

    def get_queryset(self):
        search = self.get_old_data('search')
        return Product.objects.filter(name__icontains=search).order_by('-name')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        return self.get_all_olds_datas(context=context, attributes=self.attributes)


class ProductDetail(DetailView,OldDataMixin):
   model = Product
   template_name = 'catalogs/detail.html'
   def get_context_data(self, **kwargs):
       context = super(ProductDetail, self).get_context_data(**kwargs)
       form=CartAdd()
       context['form']=form
       DataUser(self,self.request,context)
       return context


# class UpdatePerfilView(UpdateView):
class Prueba(DetailView,OldDataMixin):
    #vista de Home de Aplicación
   model = Product
   template_name = 'catalogs/detail1.html'

   def get_context_data(self, **kwargs):
       context = super(Prueba, self).get_context_data(**kwargs)
       form=CartAdd()
       context['form']=form
       DataUser(self,self.request,context)
       return context



def product_detail(request, id):
    product = get_object_or_404(Product,id=id, available = True, status=True)
    form = CartAddProductForm()
    print(product.characteristic.all())
    return  render(request,'products/detail.html',{'product':product,'form':form})