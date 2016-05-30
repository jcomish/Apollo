from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^employees', views.add_emp, name='add_emp'),
    url(r'^stores$', views.add_stores, name='add_stores'),
    url(r'^msg$', views.add_msg_types, name='add_msg_types'),
    url(r'^status', views.add_status, name='add_status'),

]
