from django.conf.urls import url, include
from .views import current_listing


urlpatterns = [
    url(r'^$', current_listing, name='current_listing')
]