
from pprint import pprint
import datetime
import json

import requests
from requests.exceptions import HTTPError



def make_get_request(url):
    try:
        response = requests.get(url)

        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print('Success!')
        print(f'status code: {response.status_code}')
        print('\nresult:')

    return response.text


url = "https://www.example.com"
#url = "https://jsonplaceholder.typicode.com/todos/1"

# this is a simple get request that returns '200 OK'
url = 'https://httpstat.us/200'
#url = 'https://superfish.badssl.com'
#url = 'https://api.github.com'
#url = 'https://api.github.com/invalid'
#url = 'https://google.com'
begin_date = datetime.datetime.now().strftime("%Y%m%d") # (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d")
time_range = 48
station = 9446491
product = 'predictions'
interval = 'hilo'  # some stations can only provide hilo
units = 'english'  # metric
print(f'begin_date: {begin_date}')

#url = 'https://tidesandcurrents.noaa.gov/api/datagetter?date=today&product=predictions&datum=mllw&interval=hilo&format=json&units=metric&time_zone=lst_ldt&station=9446491'

#url = f'https://tidesandcurrents.noaa.gov/api/datagetter?date=today&product={product}&datum=mllw&interval={interval}&format=json&units={units}&time_zone=lst_ldt&station={station}'

url = f'https://tidesandcurrents.noaa.gov/api/datagetter?begin_date={begin_date}&range={time_range}&product={product}\
&datum=mllw&interval={interval}&format=json&units={units}&time_zone=lst_ldt&station={station}'

url = "&".join(('https://tidesandcurrents.noaa.gov/api/datagetter?time_zone=lst_ldt',
    f'station={station}',
    f'begin_date={begin_date}',
    f'range={time_range}',
    'product=predictions',
    'datum=mllw',
    'interval=hilo',
    'format=json',
    'units=metric',
    ))

url = "https://plyolddogsreading.com "


tide_prediction = make_get_request(url)

print(tide_prediction)

tide_prediction = json.loads(tide_prediction)

for item in tide_prediction.get('predictions'):
    time = item.get('t')
    time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M')
    print(f"{time.strftime('%l:%M %p')}: {item.get('type')}, {item.get('v')}")






