import json
import os
from unittest.mock import patch

from django.test import TestCase
from restless.constants import BAD_REQUEST, OK


class WeatherResourceTest(TestCase):
    def test_weather_data_bad_request(self):
        resp = self.client.get(
            path='/api/weatherconnect/?missing_params=true'
        )
        resp_data = json.loads(resp.content.decode('utf-8'))
        self.assertEqual(resp_data['error'],
                         "The query should contain 3 "
                         "parameters: city, start_date, end_date")
        self.assertEqual(resp.status_code, BAD_REQUEST)

    @patch('weatherconnect.utils.get_external_data')
    def test_weather_data_bad_OK(self, mock_external_call):
        with open(os.path.join('tests', 'weatherconnect', 'data', 'data.json'
                               ), 'r') as f:
            mock_external_call.return_value = json.loads(f.read())
            resp = self.client.get(
                path='/api/weatherconnect/?city=london&'
                     'start_date=2013-05-06T20:00:00&'
                     'end_date=2013-05-06T20:00:00'
            )

            resp_data = json.loads(resp.content.decode('utf-8'))
            self.assertDictEqual(
                resp_data,
                {'average_humidity': 0.575,
                 'average_temperature': 16,
                 'max_humidity': 0.85,
                 'max_temperature': 21,
                 'median_humidity': 0.6141666666666666,
                 'median_temperature': 16,
                 'min_humidity': 0.41,
                 'min_temperature': 11,
                 'period': '2013-05-06T20:00:00 to 2013-05-06T20:00:00'}
            )
            self.assertEqual(resp.status_code, OK)
