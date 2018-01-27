from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.home_page),
    url(r'^registration$',views.register),
    url(r'^login$', views.login),
    url(r'^inventory/(?P<id>\d+)$', views.inventory, name="inventory"),
    url(r'^update$', views.update),
    url(r'^update_page/(?P<id>\d+)$', views.update_page, name="update_page")
]
