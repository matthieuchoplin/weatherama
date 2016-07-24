from django.conf.urls import url, include

from weatherconnect.api import WeatherResource
from weatherconnect import views

urlpatterns = [
    url(r'api/weatherconnect/', include(WeatherResource.urls())),
    url(r'^$', views.home, name='home'),
    url(r'^discretebarchart/', views.weather_discretebarchart,
        name='demo_discretebarchart'),
]
