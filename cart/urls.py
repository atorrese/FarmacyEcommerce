from django.urls import path
from django.conf.urls import url
import cart.views as cart
from cart import views



urlpatterns = [
    path(route='detail/',view=cart.ListCart.as_view() , name='cart_detail'),
    path(route='add/prueba/<int:pk>/',view =cart.CreateCart.as_view(), name='cart_prueba'),
    path(route='edit/<int:pk>',view =cart.Update.as_view(), name='cart_edit'),
    path(route='add/',view =cart.Create.as_view(), name='cart_add'),
    path(route='remove/<int:pk>/',view=cart.Delete.as_view() , name='remove'),
]