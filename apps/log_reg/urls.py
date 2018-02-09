from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.home_page),
    url(r'^registration$',views.register),
    url(r'^login$', views.login),
    url(r'^inventory/(?P<id>\d+)$', views.inventory, name="inventory"),
    url(r'^inventory/location/(?P<location>[a-zA-z0-9-]*)$', views.location),
    url(r'^inventory/product_name/(?P<pname>[a-zA-z0-9 -]*)$', views.pname),
    url(r'^update$', views.update),
    url(r'^update_page/(?P<id>\d+)$', views.update_page, name="update_page"),
    url(r'^profile/(?P<id>\d+)$', views.profile, name='profile'),
    url(r'^profile_update/(?P<id>\d+)$', views.profile_update),
    url(r'^logout$', views.logout)
]
