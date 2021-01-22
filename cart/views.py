from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import  JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView, DeleteView,UpdateView
from django.views.generic.base import View

from FarmacyEcommerce.funciones import DataUser
from orders.forms import OrderForm
from orders.models import Client
from utils.mixins import OldDataMixin
from .models import Cart


from catalog.models import Product, Images
from .forms import  CartAddProductForm, CartAdd,CartForm

from orders.views import  OrderCreate

class Create(LoginRequiredMixin,CreateView, OldDataMixin):
    model = Cart
    form_class = CartForm
    def get_context_data(self, **kwargs):
        context = super(Create, self).get_context_data(**kwargs)
        context['ruta'] = self.request.path
        return  context
    
    def form_valid(self, form):
        cart = form.save(commit= False)
        if self.request.is_ajax():
            if self.request.user.is_authenticated:
                cart_act= self.model.objects.filter(user=self.request.user,product = cart.product)
                if cart_act.exists():
                    cart_act = cart_act.get(user=self.request.user,product = cart.product)
                    cart_act.quantity += cart.quantity
                    cart = cart_act
                    print(cart_act.quantity)
                    
                cart.price = cart.product.price
                cart.user = self.request.user
                cart.save()
                return JsonResponse({'resp': 'ok','nameProduct':cart.product.name})
            else:
               return JsonResponse({'resp':'err','msg':'Debe Logearse'})

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'resp':'erorr'})
        return redirect('cart:cart_detail')

class Update(LoginRequiredMixin,UpdateView, OldDataMixin):
    model = Cart
    form_class = CartForm
    def get_context_data(self, **kwargs):
        context = super(Update, self).get_context_data(**kwargs)
        context['ruta'] = self.request.path
        return  context

    def form_valid(self, form):
        cart = form.save(commit= False)    
        if self.request.is_ajax():
            if self.request.user.is_authenticated:
  
                cart.save()
                return JsonResponse({'resp':'ok','msg':'Todo bien','nameProduct':cart.product.name})
            else:
               return JsonResponse({'resp':'err','msg':'Debe Logearse'})

class Delete(LoginRequiredMixin,DeleteView):
    model = Cart

    def post(self, request, *args, **kwargs):
        a = self.get_object()
        self.get_object().delete()
        data = {
            'resp': 'ok',
            'nameProduct': a.product.name
        }
        return JsonResponse(data)






class CreateCart(LoginRequiredMixin,CreateView, OldDataMixin):
    model = Cart
    form_class = CartAdd

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'resp':'erorr'})
        return redirect('cart:cart_detail')

    def form_valid(self, form):
        self.product = Product
        cart = form.save(commit=False)
        if self.request.user.is_authenticated:
            cart_product_exists = self.model.objects.filter(user=self.request.user,product__id=self.kwargs['pk'])

            if cart_product_exists.exists():
                cartq=cart_product_exists.get(user =self.request.user, product__id=self.kwargs['pk'])

                if self.request.is_ajax():
                    cartq.quantity = self.request.POST['quantity']
                    cartq.save()
                    nameprod= cartq.product.name

                    return JsonResponse({'resp': 'ok','nameProduct':nameprod})

                cartq.quantity += cart.quantity
                cartq.save()
                return redirect('/catalog/{}/detail'.format(cartq.product.id))

            cart.user = self.request.user
            cart.url = ''
            cart.product = self.product.objects.get(id=self.kwargs['pk'])
            cart.price = cart.product.price
            form.save()
        return redirect('/catalog/{}/detail'.format(cart.product.pk))


    def get_context_data(self, **kwargs):
        context = super(CreateCart, self).get_context_data(**kwargs)
        context['ruta'] = self.request.path
        return  context

class ListCart(ListView,OldDataMixin):
    model = Cart
    template_name = 'cart/detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ListCart,self).get_context_data(**kwargs)
        DataUser(self,self.request,context)
        context['form'] = CartAdd()
        return context







@require_POST
def cart_add(request, product_id):
    cartO = CartObject(request)
    product = get_object_or_404(Product,id= product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        if request.user.is_authenticated:
            itemcart = Cart.objects.filter(user=request,product=product)
            if not itemcart.exists():
                item = Cart(
                    product=product,
                    user = request.user,
                    quantity= int(cd['quantity']),
                    price = product.price,
                )
                item.save()
            itemcart.update(
                quantity=int(cd['quantity']),
                price=product.price,
            )
        else:
            cartO.add(product = product,
                     quantity=int(cd['quantity']),
                     update_quantity=cd['update'])
    return redirect('cart:cart_detail')



def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form']= CartAddProductForm(initial={'quantity':item['quantity'],'update':True})

    return render(request, 'cart/detail.html',{'cart':cart})
#ESto ya no uso

def add_cart(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)

    cart.add(product=product,quantity=['quantity'])
    return JsonResponse({'cart':product})


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product,id = product_id)
    cart.remove(product)
    return  redirect('cart:cart_detail')

