from django.conf.urls import url, include
from accounts.views import logout, login, register, user_portfolio, sell_shares, sell_commodities, update_user, delete_user

urlpatterns = [
    url(r'^logout/$', logout, name='logout'),
    url(r'^login/$', login, name='login'),
    url(r'^register/$', register, name='register'),
    url(r'^portfolio/$', user_portfolio, name='portfolio'),
    url(r'^sell_shares/(?P<id>\d+)', sell_shares, name='sell_shares'),
    url(r'^sell_commodities/(?P<id>\d+)', sell_commodities, name='sell_commodities'),
    url(r'^update_user/$', update_user, name='update_user'),
    url(r'^delete_user/$', delete_user, name='delete_user')
]
