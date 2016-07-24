import json
from unittest.mock import patch, MagicMock

from django.test import RequestFactory, TestCase
from django.core.urlresolvers import resolve

from weatherconnect.views import home

from restless.exceptions import BadRequest


class HomePageTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super(HomePageTests, cls).setUpClass()
        request_factory = RequestFactory()
        cls.request = request_factory.get('/')
        cls.request.session = {}

    def test_root_resolve_to_main_view(self):
        main_page = resolve('/')
        self.assertEqual(main_page.func, home)

    def test_return_appropriate_html(self):
        resp = home(self.request)
        self.assertEqual(resp.status_code, 200)

    def test_uses_index_html_template(self):
        index = self.client.get('/')
        self.assertTemplateUsed(index, "home.html")

    @patch('weatherconnect.utils.get_external_data', MagicMock())
    def test_post_home_return_chart_bar(self):
        data = {
            'city': 'London',
            'start_date': '05-06-2013',
            'end_date': '05-06-2013',
        }
        resp = self.client.post(
            '/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 200)

    @patch('weatherconnect.utils.get_external_data', side_effect=BadRequest)
    def test_post_home_return_error_message(self, mock):
        data = {
            'city': 'London',
            'start_date': '05-06-2013',
            'end_date': '05-06-2013',
        }
        resp = self.client.post(
            '/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 200)
