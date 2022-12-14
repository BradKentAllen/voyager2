# basic script for testing API's


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

url = 'https://api.weather.gov/gridpoints/TOP/31,80/forecast'

# this returns the grid location using lat/long
url = 'https://api.weather.gov/points/39.7456,-97.0892'

url = "https://api.nytimes.com/svc/topstories/v2/home.json?api-key=5S41B1P6Ht6BjdRVbe3nCzekNuSvDaR0"


response_text = make_get_request(url)

#print(response_text)

json_data = json.loads(response_text)

results = json_data.get('results')

data = results[0]

print(f"headline:\n{data.get('title')}\n")

print('\ndata:')
pprint(data)





