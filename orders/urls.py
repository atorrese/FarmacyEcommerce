from django.urls import  path
from django.conf.urls import url
from . import views

import orders.payment.views as Payment
urlpatterns = [
    path(route='index/',view= views.OrderList.as_view() , name='orders.index'),
    path(route='create/',view = views.OrderCreate.as_view() , name='orders.create'),
    
    path(route='process/<int:pk>/',view= Payment.ProcessPyment.as_view() , name='payment.process'),
    path(route='done/',view= Payment.payment_done, name='payment.done'),
    path(route='canceled/', view = Payment.payment_canceled, name='payment.canceled'),
    # path('admin/order/<int:order_id>/pdf/', views.admin_order_pdf, name='admin_order_pdf'),

]
app_name = 'orders'
