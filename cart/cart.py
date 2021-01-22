from decimal import Decimal

from django.conf import  settings

from catalog.models import Product

class Cart(object):
    def __init__(self,request):
        '''Constructor Inicializacion del Carrito Compras'''

        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            #Si no Existe un carro guarda uno en  la session
            cart = self.session[settings.CART_SESSION_ID]={}
        self.cart =cart

    def __iter__(self):

        product_ids = self.cart.keys()

        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product']=product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Cuenta todos los items que estan en el carrito"""
        return sum(item['quantity'] for item in self.cart.values())

    def add(self,product,quantity = 1, update_quantity = False):
        product_id = str(product.id)
        if not product_id in self.cart:
            self.cart[product_id]= {'quantity':0,'price': str(product.price)}
        if update_quantity :
            self.cart[product_id]['quantity'] =  quantity
        else:
            self.cart[product_id]['quantity'] +=  quantity

        self.save()

    def save(self):
        self.session.modified= True

    def remove(self,product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
        print('Removido')

    def get_total_price (self):
        return  sum(Decimal(item['price'])* item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()