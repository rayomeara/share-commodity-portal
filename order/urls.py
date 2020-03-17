from django.conf.urls import url
from .views import view_order, add_to_share_order
from .views import adjust_share_order, add_to_commodity_order
from .views import adjust_commodity_order

urlpatterns = [
    url(r'^$', view_order, name='view_order'),
    url(r'^addshare/(?P<id>\d+)', add_to_share_order, name='add_to_share_order'),
    url(r'^adjustshare/(?P<id>\d+)', adjust_share_order, name='adjust_share_order'),
    url(r'^addcommodity/(?P<id>\d+)', add_to_commodity_order, name='add_to_commodity_order'),
    url(r'^adjustcommodity/(?P<id>\d+)', adjust_commodity_order, name='adjust_commodity_order'),
]