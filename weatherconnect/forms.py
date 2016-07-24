from django.forms import ModelForm
from .models import Weather
from django import forms
from functools import partial
DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class HomeForm(ModelForm):
    city = forms.CharField()
    start_date = forms.DateTimeField(widget=DateInput())
    end_date = forms.DateTimeField(widget=DateInput())

    class Meta:
        fields = ['city', 'start_date', 'end_date']
        model = Weather
