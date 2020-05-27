from django.conf.urls import url
from .views import show_performance, line_chart_json

urlpatterns = [
    url(r'^$', show_performance, name='show_performance'),
    url('chartJSON', line_chart_json, name='line_chart_json'),
]
