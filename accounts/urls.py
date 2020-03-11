from django.conf.urls import url, include
from accounts.views import logout, login, register, user_portfolio

urlpatterns = [
    url(r'^logout/$', logout, name='logout'),
    url(r'^login/$', login, name='login'),
    url(r'^register/$', register, name='register'),
    url(r'^portfolio/$', user_portfolio, name='portfolio')
]
