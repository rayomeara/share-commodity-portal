from django.conf.urls import url
from .views import show_performance

urlpatterns = [
    url(r'^$', show_performance, name='show_performance'),
]