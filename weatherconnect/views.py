# -*- coding: utf-8 -*-
from collections import OrderedDict
from django.contrib import messages
from django.http import HttpResponse

from django.shortcuts import render_to_response
from django.template import loader
from restless.exceptions import BadRequest

from .forms import HomeForm

from .api import WeatherResource


def home(request):
    if request.method == 'POST':
        form = HomeForm(request.POST)
        if form.is_valid():
            our_form = form.save(commit=False)

            request.GET = {
                'city': our_form.city,
                'start_date': our_form.start_date.strftime('%d-%m-%Y'),
                'end_date': our_form.end_date.strftime('%d-%m-%Y')
            }
            try:
                return weather_discretebarchart(request)
            except BadRequest as e:
                messages.error(request, str(e))
    else:
        form = HomeForm()
    t = loader.get_template('home.html')
    return HttpResponse(t.render({'form': form, }, request))


def weather_discretebarchart(request):
    city = request.GET.get('city')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    weather = WeatherResource()
    weather.request = request
    resp_data = weather.weather_data()
    resp_data.pop('period')
    resp_data = OrderedDict(sorted(resp_data.items(), key=lambda t: t[0]))
    xdata, ydata = [], []
    for x, y in resp_data.items():
        xdata.append(x.replace('_', ' ').capitalize())
        ydata.append(y)
    extra_serie1 = {"tooltip": {"y_start": "", "y_end": " cal"}}
    chartdata = {
        'x': xdata,
        'name1': '',
        'y1': ydata,
        'extra1': extra_serie1,
    }
    charttype = "discreteBarChart"
    chartcontainer = 'discretebarchart_container'  # container name
    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,
        'extra': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': True,
            'chart_attr': {
                'xAxis.rotateLabels': '-35',
                'margin': '{bottom: 80, left: 30}',
            },
        },
        'city': city.capitalize(),
        'start_date': start_date,
        'end_date': end_date,
    }
    return render_to_response('discretebarchart.html', data)
