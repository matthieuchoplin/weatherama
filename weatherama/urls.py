from django.conf.urls import patterns, url, include

from weatherconnect.api import WeatherResource

urlpatterns = [
    url(r'api/weatherconnect/', include(WeatherResource.urls())),
]
