from django.conf.urls import url, include
from . import views

urlpatterns = [
    #RENDER ROUTES
    url(r'^$', views.index),
    url(r'^login$', views.login_page),
    url(r'^register$', views.register_page),
    url(r'^dashboard$', views.dashboard_page),
    url(r'^admin$', views.admin_page),
    url(r'^users/(?P<id>\d+)/$', views.profile_page),
    url(r'^users/edit/$', views.user_edit_page),
    url(r'^admin/edit/(?P<id>\d+)$', views.admin_edit_page),
    url(r'^admin/add/$', views.admin_add_page),

    #PROCESS ROUTES
    url(r'^login_process$', views.login_process),
    url(r'^register_process$', views.register_process),
    url(r'^logout_process$', views.logout_process),
    url(r'^message_process/(?P<id>\d+)$', views.message_process),
    url(r'^comment_process/(?P<msg_id>\d+)$', views.comment_process),
    url(r'^edit_process/(?P<id>\d+)$', views.edit_process),
    url(r'^add_process$', views.remove_process),
    url(r'^remove_process/(?P<id>\d+)$', views.remove_process),
    
]