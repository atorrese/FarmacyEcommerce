from django.urls import path
from django.conf.urls import url
import views as cart




urlpatterns = [
    path(route='detail/',view=cart.ListCart.as_view() , name='cart_detail'),
    path(route='add/<int:pk>/',view =cart.CreateCart.as_view(), name='cart_add'),
    path(route='remove/<int:pk>/',view=cart.Delete.as_view() , name='remove'),
]