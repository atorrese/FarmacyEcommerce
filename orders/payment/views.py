import json
from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import  settings
from django.core.mail import  EmailMessage
from django.shortcuts import render,redirect,get_object_or_404
from django.template.loader import render_to_string

import braintree
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView
from django.views.generic.base import View

from utils.mixins import OldDataMixin
from FarmacyEcommerce.funciones import DataUser, DataUser2
from orders.forms import OrderForm
from orders.models import Order, OrderDetail
from paypal.standard.forms import PayPalPaymentsForm





class ProcessPyment(LoginRequiredMixin,UpdateView,OldDataMixin):
    model = Order
    form_class =  OrderForm
    def post(self, request, *args, **kwargs):
        post = super().post(request,*args,**kwargs)
        print(post)
        print(request)
        return post

    def form_valid(self, form):
        order = form.save(commit=False)
        print(self.request.POST)
        print(order)
        if self.request.is_ajax():
            try:
                self.request.session['Orden_id']= order.pk
                return JsonResponse({'resp': 'ok'})
            except Exception as e:
                return JsonResponse({'resp':'error'})

        nonce = self.request.POST.get('payment_method_nonce', None)
        result = braintree.Transaction.sale(
            {
                'amount':'{}'.format(order.get_total_cost()),
                      'payment_method_nonce':nonce,
                'options':{
                    'submit_for_settlement':True
                },
            }
        )
        if result.is_success:
            order.paid = True
            order.type_pay='Tarjeta De Credito'
            order.paypal_id = result.transaction.id
            order.save()
            #envio de Correo
            subject = 'Tienda Online "ShopMarthen" - Factura no. {}'.format(order.id)
            message = '''
                        Usted Realizo una  Pedido   y pago con {}\n
                        el valor de ${} \n\n
                        Direccion de entrega: {}\n
                        Detalle De Productos\n
                        
                        Producto -----         Cantidad --- Precio ---- Total\n
                        '''.format(order.type_pay,order.get_total_cost(),order.client.address)

            details = OrderDetail.objects.filter(order=order)
            for o in details:
                message += '''{}               {}     ${}          ${}\n
                            '''.format(o.product.name,o.quantity,o.price,o.get_cost())

            email = EmailMessage(subject,
                                 message,
                                 to=[order.client.user.email])

            email.send()
            return redirect('order:payment.done')
        else:
            message = result.message

            self.request.session['dataError']= {'message':message}
            return redirect('order:payment.canceled')

    def form_invalid(self, form):
        print(form)
        return redirect('order:payment.canceled')

    def get_context_data(self, **kwargs):
        context = super(ProcessPyment,self).get_context_data(**kwargs)
        DataUser(self, self.request, context)
        host = self.request.get_host()
        order= self.get_object()
        print(order)
        print(order.get_total_cost())
        paypal_dict = {
            'business':settings.PAYPAL_RECEIVER_EMAIL,
            'amount':'%.2f'%order.get_total_cost(),
            'item_name':'Orden {}'.format(str(order.pk)),
            'invoice':str(order.pk),
            'currency_code':'USD',
            'notifi_url':self.request.build_absolute_uri(reverse('paypal-ipn')),
            'return':self.request.build_absolute_uri(reverse('order:payment.done')),
            'cancel_return':self.request.build_absolute_uri(reverse('order:payment.canceled')),

        }
        form = PayPalPaymentsForm(initial=paypal_dict)
        context['form_paypal']=form
        client_token = braintree.ClientToken.generate()
        user = self.request.user
        context['client_token'] = client_token
        return  context






@csrf_exempt
def payment_done(request):
    print( request.GET)
    id=request.session.get('Orden_id',None)
    print(id)
    if id !=  None :
        order = Order.objects.get(id=id)
        order.paid=True
        order.type_pay='Paypal'
        order.save()

        subject = 'Tienda Online "ShopMarthen" - Factura no. {}'.format(order.id)
        message = '''
                    Usted Realizo una  Pedido   y pago con {}\n
                    el valor de ${} \n\n
                    Direccion de entrega: {}\n
                    Detalle De Productos\n

                    Producto -----         Cantidad --- Precio ---- Total\n
                    '''.format(order.type_pay, order.get_total_cost(), order.client.address)

        details = OrderDetail.objects.filter(order=order)
        for o in details:
            message += '''{}               {}     ${}          ${}\n
                        '''.format(o.product.name, o.quantity, o.price, o.get_cost())

        email = EmailMessage(subject,
                             message,
                             to=[order.client.user.email])
        print(email)
        email.send()
        print(email)
    data = {}
    DataUser2(request, data)
    return render(request,'orders/payment/done.html',data)

@csrf_exempt
def payment_canceled(request):
    data = {}
    DataUser2(request, data)
    return render(request, 'orders/payment/canceled.html',data)

def prueba(request):
    return  render(request,'orders/prueba.html')

