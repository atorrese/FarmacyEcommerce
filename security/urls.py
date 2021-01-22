#Security Urls

# Django
from django.urls import path
from django.conf.urls import url

# Views
import security.views as security

urlpatterns = [
    path(route='', view=security.HomeView.as_view(), name='home'),
    path(route='login/', view=security.LoginView.as_view(), name='login'),
    path(route='logout/', view=security.LogoutView.as_view(), name='logout'),
    path(route='register/', view=security.RegisterView.as_view(), name='register'),
    #path(route='prueba/<int:pk>/detail', view=security.Prueba.as_view(), name='prueba'),
]