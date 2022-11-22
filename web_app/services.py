import requests
from requests.exceptions import Timeout, HTTPError
from decouple import config

def get_covalent_data(token_id, endpoint):
    base_url = 'https://api.covalenthq.com/v1'
    api_key = config('COVALENT_API_KEY')
    complete_url = f'{base_url}/{token_id}/{endpoint}'
    parameters = {'key': api_key}

    # Attempt to get data and handle errors along the way
    try:
        response = requests.get(complete_url, params=parameters, timeout=10)
        response.raise_for_status()

        return response.json()
    except Timeout as err:
        print("Request timed out:", err)
    except HTTPError as err:
        print("Http error:", err)

def get_coingecko_data(search_key):
    base_url = 'https://api.coingecko.com/api/v3/search?'
    # api_key = config('COVALENT_API_KEY')
    # complete_url = f'{base_url}/{token_id}/{endpoint}'
    parameters = {'query': search_key}

    # Attempt to get data and handle errors along the way
    try:
        response = requests.get(base_url, params=parameters, timeout=10)
        response.raise_for_status()

        return response.json()
    except Timeout as err:
        print("Request timed out:", err)
    except HTTPError as err:
        print("Http error:", err)