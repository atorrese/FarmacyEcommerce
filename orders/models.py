#Django
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
# App
#from material.frontend.templatetags.material_frontend import verbose_name_plural

#from locations.models import Canton
from catalog.models import Product
from security.models import ModelBase

from decimal import Decimal
"""     def get_cost(self):
        return self.product.price*self.quantity

    def get_total_cost(self):
        items=Cart.objects.filter(user=self.user)
        total_cost =  sum(item.get_cost() for item in items)
        return total_cost
 """
class Client(ModelBase):
    address = models.CharField(_('Direccion'), max_length=250)
    address2 = models.CharField(_('Direccion 2'), max_length=250)
    postal_code = models.CharField(_('Codigo Postal'), max_length=20)
    #canton = models.ForeignKey(Canton, on_delete=models.PROTECT)
    user = models.OneToOneField(User,on_delete=models.PROTECT)
    foto = models.FileField(upload_to='Perfiles')

    class Meta:
        verbose_name='Cliente'
        verbose_name_plural='Cliente'
        ordering = ('-created_at',)

    '''def __str__(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)

    def get_image_client(self):
        return  self.foto.url'''

class Order(ModelBase):
   client = models.ForeignKey(Client,on_delete=models.PROTECT)
   type_pay = models.CharField(_('Tipo Pago'),max_length=100)
   paid = models.BooleanField(default=False)
   paypal_id = models.CharField(max_length=150,blank=True)

   def __str__(self):
       return  'Orden {}'.format(self.id)
       
   def get_total_cost(self):
       total_cost = sum(item.get_cost() for item in self.items.all())
       return  total_cost
   
   class Meta:
       verbose_name = 'Orden'
       verbose_name_plural = 'Ordenes'
       ordering = ('-created_at',)







class OrderDetail(ModelBase):
    order = models.ForeignKey(Order,related_name='items', on_delete= models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price*self.quantity