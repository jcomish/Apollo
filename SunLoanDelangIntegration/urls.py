from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^view', views.view, name='view'),
    url(r'^verify', views.verify, name='verify'),
    url(r'^search', views.search, name='search'),
    url(r'^', views.index, name='index'),
]