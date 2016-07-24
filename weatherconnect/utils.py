from datetime import datetime
import json

from time import mktime
from urllib.request import urlopen

from django.conf import settings
from geopy.geocoders import Nominatim
import parsedatetime
from restless.exceptions import BadRequest

geolocator = Nominatim()


def date_value_in_datetime(value):
    cal = parsedatetime.Calendar()
    time_struct, parse_status = cal.parse(value)
    if parse_status == 0:
        raise BadRequest(msg='Invalid Date')
    return datetime.fromtimestamp(mktime(time_struct))


def latitude_longitude(city):
    location = geolocator.geocode(city)
    if location:
        return location.latitude, location.longitude
    else:
        raise BadRequest(msg='City {} not found'.format(city))


def get_external_data(latitude, longitude, date_datetime):
    date_unixtime = int(mktime(date_datetime.timetuple()))
    if not hasattr(settings, 'FORECAST_API_KEY'):
        raise BadRequest(msg="You need to configure the FORECAST_API_KEY")
    url = "https://api.forecast.io/forecast/" \
          "{api}/{latitude},{longitude},{date_unixtime}?units=si".format(
              api=settings.FORECAST_API_KEY,
              latitude=latitude,
              longitude=longitude,
              date_unixtime=date_unixtime
          )
    resp = urlopen(url).read().decode('utf8')
    return json.loads(resp)


def worker(lst_tp, lst_hm, latitude, longitude, date_datetime):
    obj = get_external_data(latitude, longitude, date_datetime)
    hourly_data = obj['hourly']['data']
    for hour in hourly_data:
        if 'temperature' in hour:
            lst_tp.append(hour['temperature'])
        if 'humidity' in hour:
            lst_hm.append(hour['humidity'])
