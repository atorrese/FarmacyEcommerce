from django.conf.urls import url
from django.urls import path
import catalog.category.views as category
import catalog.products.views   as product

urlpatterns = [
    path(route='', view=product.Index.as_view(), name='produts.index'),
    path(route='<int:pk>/detail', view=product.ProductDetail.as_view(), name='product.detail'),
    path(route='prueba/<int:pk>/detail', view=product.Prueba.as_view(), name='detail'),

    path(route='category/', view=category.Index.as_view(), name='category.index'),
    path(route='category/create/', view=category.Create.as_view(), name='category.index'),

]