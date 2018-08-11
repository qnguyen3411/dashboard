from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login_page),
    url(r'^register$', views.register_page),
    
]