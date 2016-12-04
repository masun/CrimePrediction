from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'), #GET todos los usuarios
    url(r'^([0-9]+)$', views.get_user), 
    url(r'login$', views.login),
    url(r'logout$', views.logout)
]