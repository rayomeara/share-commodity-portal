from django.conf.urls import url
from .views import process_payment


urlpatterns = [
    url(r'^$', process_payment, name='process_payment'),
]