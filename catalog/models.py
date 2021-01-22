from django.db import models
from django.utils.html import mark_safe

from security.models import ModelBase
#from sellers.models import Seller


class Category(ModelBase):
    name = models.CharField(max_length=110)
    image = models.ImageField(upload_to='Category')

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name_plural = 'Categorias'
        verbose_name = 'Categoria'
        ordering = ('name',)
    
    def get_icon(self):
        return  mark_safe('<img src="{}" style="width:10%" style="border-radius: 8px;"'.format(self.image.url))

class Mark(ModelBase):
    name = models.CharField(max_length=110)
    image = models.ImageField(upload_to='Mark')

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name_plural = 'Marcas'
        verbose_name = 'Marca'
        ordering = ('name',)
        
    def get_icon(self):
        return  mark_safe('<img src="{}" style="width:10%" style="border-radius: 8px;"'.format(self.image.url))
class Presentation(ModelBase):
    name = models.CharField(max_length=300)

    def __str__(self):
        return  '{}'.format(self.name)

    class Meta:
        verbose_name = 'Presentation'
        verbose_name_plural = 'Presentaciones'
        ordering = ('name',)
    


class Product(ModelBase):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    dosage = models.CharField(max_length=500,default='',null=True,blank=True)
    contraindication = models.CharField(max_length=500,default='',null=True,blank=True)
    price = models.DecimalField(max_digits=19, decimal_places=2)
    stock = models.IntegerField(default=0)
    available = models.BooleanField(default=True)
    elaboration_date = models.DateField()
    expiration_date = models.DateField()
    mark =models.ForeignKey(Mark,on_delete=models.PROTECT)
    presentation = models.ForeignKey(Presentation,on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)


    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name_plural = 'Productos'
        verbose_name = 'Producto'
        ordering = ('name',)

    def get_image(self):
        return  mark_safe('<img src="{}" style="width:20%" style="border-radius: 8px;"'.format(self.images_set.first().get_image_url()))
    
    def get_url_image(self):
        return self.images_set.first().get_image_url()
class Images(ModelBase):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    url = models.ImageField()
    name = models.CharField(max_length= 100)

    def __str__(self):
        return '{}'.format(self.name)
    class Meta:
        verbose_name_plural = 'Imagenes'
        verbose_name = 'Imagen'
        ordering = ('name',)
    
    def get_image_url(self):
        return  self.url.url

