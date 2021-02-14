import config
import requests
from urllib.parse import urlencode, quote_plus


def fetch_gifs(search_expression, results, rating):

    # search endpoint
    # https://developers.giphy.com/docs/api/endpoint#search

    url = "http://api.giphy.com/v1/gifs/search"

    params = urlencode({
        "q": search_expression,
        "api_key": config.API_KEY,
        "limit": int(results),
        "rating": rating
    })


    # print(params)

    url = url + '?' + params

    r = requests.get(url).json()

    # print(r)

    res = list()

    for item in r["data"]:
        res.append({'title': item['title'], 'gif_url': item['images']['original']['mp4']})

    # print(res)
    return res
