# django
import os

from django.contrib.auth.models import User
from django.db.models import Q, Max, Min

from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView, DetailView, ListView, CreateView, FormView, UpdateView

#from locations.models import Province, Canton
from orders.models import Client
from security.forms import RegisterForm
from django.contrib.auth.mixins import LoginRequiredMixin

from FarmacyEcommerce.funciones import DataUser
from utils.mixins import OldDataMixin

from catalog.models import Product,Mark


class HomeView(LoginRequiredMixin, ListView, OldDataMixin):
    #vista de Home de Aplicación
    model = Product
    context_object_name = 'products'
    template_name = 'auth/home.html'
    attributes = {'search': '','s_mark':'','s_price_i':'','spric_f':''}
    paginate_by = 6

    def get_queryset(self):
        search = self.get_old_data('search')
        if 's_mark' in self.request.GET:
            return  Product.objects.filter(mark=self.get_old_data('s_mark'))
        s_price_i =self.get_old_data('s_price_i')
        s_price_f =self.get_old_data('s_price_f') 
        if s_price_i and s_price_f:
            return Product.objects.filter(price__range=[s_price_i,s_price_f])
        return Product.objects.filter(
            (
                Q(category__name__icontains=search) |
                Q(name__icontains=search) |
                Q(presentation__name__icontains=search)|
                Q(mark__name__icontains=search)

            )
        )
    def get_stock(self):
        return Product.objects.filter(stock__lte=5)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        context['marks'] = Mark.objects.all()
        context['max'] = Product.objects.aggregate(Max('price'))
        context['down_stock'] = self.get_stock()
        context['min'] = Product.objects.aggregate(Min('price'))
        DataUser(self, self.request, context)

        return context


@login_required()
def Index(request):
    datos = {'products': Product.objects.filter(status=True, )}


class LoginView(auth_views.LoginView):
    '''Clase Based View para Logear un usuario'''
    template_name = 'auth/login.html'
    redirect_authenticated_user = True


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    '''Clase Base View para Logout un usuario'''
    pass


class RegisterView(FormView):
    template_name = 'auth/register.html'
    form_class = RegisterForm

    success_url = '/login/'

    def form_valid(self, form):
        f = super(RegisterView, self).form_valid(form)
        print(form.cleaned_data['username'])
        user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'],
                                        form.cleaned_data['password'])
        user.first_name = form.cleaned_data['firstname']
        user.last_name = form.cleaned_data['lastname']
        user.save()
        perfil = form.cleaned_data['perfil']
        address = form.cleaned_data['address']
        cliente = Client( address=address, user=user)
        cliente.foto = perfil
        cliente.save()
        return f #redirect(self.get_success_url())

    def form_invalid(self, form):
        print(form)
        return super(RegisterView, self).form_invalid(form)

    def get(self, request, *args, **kwargs):
        get = super(RegisterView, self).get(self, request, *args, **kwargs)
        if self.request.is_ajax():
            if 'p' in self.request.GET:
                response = Province.objects.filter(country__id=self.request.GET['p'])
            if 'pro' in self.request.GET:
                response = Canton.objects.filter(province__id=self.request.GET['pro'])
            json = [{'id': resp.id, 'name': resp.name} for resp in response]
            return JsonResponse({'resp': 'ok', 'data': json})
        return get

