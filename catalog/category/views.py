'''Categories Views'''

#Django
from django.http import  JsonResponse
from django.urls import  reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,CreateView, UpdateView, DeleteView
#App
from utils.mixins import OldDataMixin
from catalog.category.forms import CategoryForm
from catalog.models import Category

class Index(LoginRequiredMixin, ListView, OldDataMixin):
    '''Lista de Categiras'''
    template_name = 'products/categories/index.html'
    model = Category
    paginate_by = 15
    context_object_name = 'categories'
    attributes = {'search':''}

    def get_queryset(self):
        search = self.get_old_data('search')
        return Category.objects.filter(name__icontains=search).order_by('-created_at')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Index,self).get_context_data(**kwargs)
        return self.get_all_olds_datas(context=context,attributes=self.attributes)

class Create(LoginRequiredMixin,CreateView,OldDataMixin):
    '''Crea Cateoria '''
    model = Category
    template_name = 'products/categories/create.html'
    form_class =  CategoryForm
    success_url = reverse_lazy('products:category.index')
    attributes = {'name':'','image':''}

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context= super(Create,self).get_context_data(**kwargs)
        return self.get_all_olds_datas(context=context,attributes=self.attributes)

class Update(LoginRequiredMixin, UpdateView, OldDataMixin):
    """Actualiza una provincia"""
    model = Category
    template_name = 'products/categories/edit.html'
    form_class = CategoryForm
    success_url = reverse_lazy('products:category.index')

    def get_attributes(self):
        return {
            'name': self.get_object().name,
            'image': self.get_object().image
        }

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(Update, self).get_context_data(**kwargs)
        return self.post_all_olds_datas(context=context, attributes=self.get_attributes())



class Delete(LoginRequiredMixin, DeleteView):
    """Elimina una provincia"""
    model = Category
    http_method_names = ['delete']

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        data = {
            'message': '¡El registro ha sido eliminado correctamente!'
        }
        return JsonResponse(data)
