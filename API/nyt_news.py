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

API_key = '5S41B1P6Ht6BjdRVbe3nCzekNuSvDaR0'
section = 'home'
url = f"https://api.nytimes.com/svc/topstories/v2/{section}.json?api-key={API_key}"


#url = f"https://api.nytimes.com/svc/news/v3/content/all/all.json?api-key={API_key}"


response_text = make_get_request(url)

print(response_text)



json_data = json.loads(response_text)

results = json_data.get('results')

print('\n\n')
for item in results:
    print(f"\n{item.get('section')}: {item.get('title')}")
    #print(f'\n{item}')

data = results[0]

print(f"headline:\n{data.get('title')}\n")

#print('\ndata:')
#pprint(data)





