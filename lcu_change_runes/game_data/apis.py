import requests


def API_GET(url):
    response = requests.get(url)
    return response.json()
