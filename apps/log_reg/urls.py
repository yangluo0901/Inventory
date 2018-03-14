from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.home_page),
    url(r'^registration$',views.register),
    url(r'^login$', views.login),
    url(r'^inventory/(?P<id>\d+)$', views.inventory, name="inventory"),
    url(r'^inventory/location/(?P<location>[a-zA-z0-9-]*)$', views.location),
    url(r'^inventory/product_name/(?P<pname>[a-zA-z0-9 -\.&]*)$', views.pname),
    url(r'^inventory/lot_number/(?P<lot_num>[a-zA-z0-9 -\.&]*)$', views.lot_num, name="lot_num"),
    url(r'^update$', views.update),
    url(r'^update_page/(?P<id>\d+)$', views.update_page, name="update_page"),
    url(r'^profile/(?P<id>\d+)$', views.profile, name='profile'),
    url(r'^profile_update/(?P<id>\d+)$', views.profile_update),
    url(r'^logout$', views.logout),
    url(r'^inventory/delete$', views.delete),
    url(r'^inventory/edit$',views.edit),
    url(r'^inventory/action/(?P<lot_num>[a-zA-z0-9 -\.&]*)$',views.action)
]
