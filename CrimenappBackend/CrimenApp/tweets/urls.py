from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^load$', views.load, name='load'),
    url(r'^textSize$', views.textSize, name="textSize")
]