from django.conf.urls import url, include
from . import views

urlpatterns = [
    #RENDERING
    url(r'^$', views.index),
    url(r'^login$', views.login_page),
    url(r'^register$', views.register_page),
    url(r'^dashboard$', views.dashboard_page),
    url(r'^admin$', views.admin_page),
    url(r'^users/(?P<id>\d+)/$', views.profile_page),

    #PROCESSING
    url(r'^login_process$', views.login_process),
    url(r'^register_process$', views.register_process),
    url(r'^logout_process$', views.logout_process),
    url(r'^message_process/(?P<id>\d+)$', views.message_process),
    url(r'^comment_process/(?P<msg_id>\d+)$', views.comment_process),
    
]