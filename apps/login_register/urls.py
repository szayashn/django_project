from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^logout$', views.logout),
    url(r'^post$', views.post),
    url(r'^post_comment$', views.post_comment),
    url(r'^delete$', views.delete_comment),
]