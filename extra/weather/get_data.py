"""
Load data from OpenWeatherMap.

You can obtain a free API key there and add it as an evironment variable,
or pass it on as a argument to the script.

The default lat lon are 47.996093, 7.853091, which is the
Freiburger Münster.
"""
from datetime import datetime as dt
from datetime import timedelta as td
import requests
import json
import os

LAT = 47.996093
LON = 7.853091
HISTORIC_URL = 'https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={lon}&dt={ts}&appid={key}'
FORECAST_URL = 'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={part}&appid={key}'

def __get_api_key(api_key):
    if api_key is None:
        api_key = os.environ.get('OWM_API_KEY')
    if api_key is None:
        raise ValueError('No OWM_API_KEY environment variable or --api-key flag found.')
    return api_key


def get_last_days(api_key=None, lat=None, lon=None, days_back=1, **kwargs):
    """
    Fetch the history data of the past day using
    the given api key
    """
    # get the API key
    key = __get_api_key(api_key)

    # get coordinates
    if lat is None:
        lat = LAT
    if lon is None:
        lon = LON

    # create UNIX timestamp, UTC
    ts = int((dt.utcnow() - td(days=days_back)).timestamp())

    # build url
    url = HISTORIC_URL.format(lat=lat, lon=lon, ts=ts, key=key)

    # load data
    response = requests.get(url)
    return json.loads(response.content)


def get_forecast(api_key=None, lat=None, lon=None, exclude_parts=['current', 'minutely', 'daily'], **kwargs):
    # get the API key
    key = __get_api_key(api_key)

    # get coordinates
    if lat is None:
        lat = LAT
    if lon is None:
        lon = LON

    # build url
    url = FORECAST_URL.format(lat=lat, lon=lon, part=','.join(exclude_parts), key=key)

    # load data
    response = requests.get(url)
    return json.loads(response.content)


def run(**kwargs):
    today = dt.now().date()
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
    fname = '{y}_{m}_{d}_raw_dump.json'.format(y=today.year, m=today.month, d=today.day)

    # load data
    hist = get_last_days(**kwargs)
    fore = get_forecast(**kwargs)

    # set error if no data
    if len(hist.keys()) == 0:
        hist = {'error': 'No data received', 'dt': dt.utcnow().isoformat()}
    if len(fore.keys()) == 0:
        fore = {'error': 'No data received', 'dt': dt.utcnow().isoformat()}

    data = {'historic': hist, 'forecast': fore}

    with open(os.path.join(path, fname), 'w') as f:
        json.dump(data, f, indent=4)

    # return for reuse
    return data

if __name__=='__main__':
    import fire
    fire.Fire({
        'last-day': get_last_days,
        'forecast': get_forecast,
        'run': run
    })