from django.conf.urls import url, include
import tellme.urls

from . import views

urlpatterns = [
    url(r'^view/', views.view, name='view'),
    url(r'^code/', views.code, name='code'),
    url(r'^contract/', views.contract, name='contract'),
    url(r'^history/', views.history, name='history'),
    url(r'^update/', views.update, name='update'),
    url(r'^verify', views.verify, name='verify'),
    url(r'^search', views.search, name='search'),
    url(r'^$', views.index, name='index'),
    url(r'^(?P<customer>[\w-]+)/$', views.index, name='index'),
]

