[![Build Status](https://travis-ci.org/matthieuchoplin/weatherama.svg?branch=master)](https://travis-ci.org/matthieuchoplin/weatherama)
[![Coverage Status](https://coveralls.io/repos/github/matthieuchoplin/weatherama/badge.svg?branch=master)](https://coveralls.io/github/matthieuchoplin/weatherama?branch=master)

To start the project in development mode:

```
sudo apt-get update
sudo apt-get install git
sudo apt-get install python-pip python3 python3-dev libpq-dev
sudo pip install virtualenv
virtualenv venv -p  /usr/bin/python3
source venv/bin/activate
git clone git@github.com:matthieuchoplin/weatherama.git
cd weatherama/
pip install -r requirements.txt
sudo apt-get install npm
sudo npm install -g bower
sudo ln -s /usr/bin/nodejs /usr/bin/node
./manage.py bower_install
./manage.py collectstatic --no-input
./manage.py migrate
./manage.py runserver 0.0.0.0:8002
```

=> this could be put in a Vagrantfile

In the `settings.py`, you need to populate a `FORECAST_API_KEY` 
that you will get by registering an account on https://developer.forecast.io/

Run tests with code coverage:
```
coverage3 run --source='.' manage.py test tests.weatherconnect
coverage3 report
```


