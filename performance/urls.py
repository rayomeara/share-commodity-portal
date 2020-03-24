from django.conf.urls import url

urlpatterns = [
    url(r'^$', show_performance, name='show_performance'),
]