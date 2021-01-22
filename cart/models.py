from decimal import Decimal

from django.db import models
from django.contrib.auth.models import User

from catalog.models import Product
from security.models import ModelBase


class Cart(ModelBase):
    price= models.DecimalField(max_digits=10,decimal_places=2)
    quantity =models.PositiveIntegerField(default=1)
    url = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)


    def get_cost(self):
        return self.product.price*self.quantity

    def get_total_cost(self):
        items=Cart.objects.filter(user=self.user)
        total_cost =  sum(item.get_cost() for item in items)
        return total_cost