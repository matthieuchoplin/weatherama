To start the project in development mode:

If you are on a UNIX machine with python3 and virtualenv installed:

```
virtualenv venv -p /usr/local/bin/python3
source venv/bin/activate
pip install -r requirements.txt
```

In the `settings.py`, you need to populate a `FORECAST_API_KEY` 
that you will get by registering an account on https://developer.forecast.io/

```
python manage.py migrate
python manage.py runserver
```
