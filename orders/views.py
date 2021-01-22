#Django
from decimal import Decimal
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
#App
from catalog.models import Images
from utils.mixins import OldDataMixin
from FarmacyEcommerce.funciones import DataUser
from orders.forms import OrderForm
from cart.models  import Cart
from .models import OrderDetail, Order, Client
from catalog.models import Product
from django.views.generic import CreateView, ListView

from django.contrib.admin.views.decorators import staff_member_required



class OrderList(LoginRequiredMixin,ListView,OldDataMixin):
    model = Order
    template_name = 'orders/order/index.html'
    attributes = {'search': ''}
    context_object_name = 'orders'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(OrderList,self).get_context_data(**kwargs)
        DataUser(self, self.request, context)
        return  self.get_all_olds_datas(context=context, attributes=self.attributes)

    def get_queryset(self):
        search = self.get_old_data('search')
        return Order.objects.filter(client__user=self.request.user,type_pay__icontains=search).order_by('-created_at')

    def get(self, request, *args, **kwargs):
        get= super().get(request,*args,**kwargs)
        if self.request.is_ajax():
            try:
                detalle={}
                detalleorder= OrderDetail.objects.filter(order__id=self.request.GET['id'])


                detalle = [{'name':item.product.name ,
                            'img':Images.objects.filter(product=item.product)[0].get_image_url(),
                            'precio':item.price,
                            'cantidad':item.quantity,
                            'total':item.get_cost()}
                           for item in detalleorder]
                total = Order.objects.get(pk=self.request.GET['id']).get_total_cost()
                return JsonResponse({'resp':'ok','detalle':detalle,'total':total})
            except Exception as e:
                return JsonResponse({'resp': 'error'})
        return get




class OrderCreate(LoginRequiredMixin,CreateView,OldDataMixin):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order/create.html'
    def form_valid(self, form):
        order = form.save(commit=False)
        #Guardando El Pedido realizado
        order.save()
        self.cart =Cart
        self.cart = self.cart.objects.filter(user=self.request.user)
        #Guardando el Detalle del pedido
        for car in self.cart:
            orderDetail = OrderDetail(
                order=order,
                product= car.product,
                price= car.product.price,
                quantity=car.quantity
            )
            orderDetail.save()
            product= Product.objects.get(id=orderDetail.product.id)
            print(product.name)
            product.stock  -= orderDetail.quantity
            product.save()
            print(product.stock)
        print(order.pk)
        #limpiar el Carror
        self.cart.delete()
        return redirect('/order/process/{}/'.format(order.pk))

    def form_invalid(self, form):
        print(form)
        return redirect('/order/create/')


    def get_context_data(self, **kwargs):
        context = super(OrderCreate,self).get_context_data(**kwargs)
        DataUser(self, self.request, context)
        return  context




