import statistics
from datetime import timedelta
from multiprocessing import Manager, Process

from django.conf.urls import url
from restless.dj import DjangoResource
from restless.exceptions import BadRequest
from .utils import date_value_in_datetime, latitude_longitude, worker


class WeatherResource(DjangoResource):
    http_methods = {
        'weather_data': {
            'GET': 'weather_data',
        }
    }

    def weather_data(self):
        city = self.request.GET.get('city')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if city and start_date and end_date:
            latitude, longitude = latitude_longitude(city)
            start_date_datetime = date_value_in_datetime(start_date)
            end_date_datetime = date_value_in_datetime(end_date)
            interval_of_days = (end_date_datetime - start_date_datetime).days
            jobs = []
            manager1 = Manager()
            lst_tp = manager1.list()
            manager2 = Manager()
            lst_hm = manager2.list()
            date_datetime = start_date_datetime
            for day in range(interval_of_days + 1):
                date_datetime += timedelta(days=day)
                p = Process(
                    target=worker,
                    args=(lst_tp, lst_hm, latitude, longitude, date_datetime)
                )
                jobs.append(p)
                p.start()
                p.join()
            return {
                'period': "{} to {}".format(start_date, end_date),
                # TEMPERATURE
                'min_temperature': round(min(lst_tp)),
                'max_temperature': round(max(lst_tp)),
                'median_temperature': round(statistics.mean(lst_tp)),
                'average_temperature': round(statistics.median(lst_tp)),
                # HUMIDITY
                'min_humidity': "{0:.0f}%".format(min(lst_hm) * 100),
                'max_humidity': "{0:.0f}%".format(max(lst_hm) * 100),
                'median_humidity': "{0:.0f}%".format(statistics.mean(
                    lst_hm) * 100),
                'average_humidity': "{0:.0f}%".format(statistics.median(
                    lst_hm) * 100),
            }
        raise BadRequest(
            msg='The query should contain 3 '
                'parameters: city, start_date, end_date'
        )


    @classmethod
    def urls(cls, name_prefix=None):
        return [
            url(r'^.*$',
                cls.as_view('weather_data'),
                name=cls.build_url_name('weather_data', name_prefix))
        ]
