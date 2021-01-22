#from cart.models import Cart
from orders.models import Client
from catalog.models import Category
from django.db.models import F , Sum
from cart.models import Cart

def DataUser(self,request,context):
    self.cart = Cart
    self.category = Category
    client = Client
    if client.objects.filter(user =request.user ).exists():    
        cliente =client.objects.get(user=request.user)
        context ['cliente']=cliente
        context ['foto']=cliente.foto.url
    carrito = self.cart.objects.filter(user=request.user)
    context['cart1']=carrito
    context['cantidad_item']=carrito.aggregate(nitems =Sum('quantity'))
    context['total_cost'] = {'total':i.get_total_cost() for i in carrito}
    context ['categories']=self.category.objects.filter(status=True)


def DataUser2(request, data):
    cliente = Client.objects.get(user =request.user)
    data['foto'] = cliente.foto.url if cliente.foto else "static/fashe-colorlib/images/icons/icon-header-01.png"
    data['categories'] = Category.objects.filter(status=True)


