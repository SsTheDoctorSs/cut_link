import os
import requests
import argparse
from urllib.parse import urlparse
from requests.exceptions import HTTPError
from dotenv import load_dotenv

API_URL = 'https://api-ssl.bitly.com/v4/'


def shorten_link(token, url):
    bitly_url = "{}shorten".format(API_URL)
    params = {"long_url": url}
    headers = {"Authorization": "Bearer {}".format(token)}
    response = requests.post(bitly_url, json=params, headers=headers)
    response.raise_for_status()
    return response.json()["link"]


def count_clicks(token, bitlink):
    bitly_url = "{0}bitlinks/{1}/clicks/summary".format(API_URL, bitlink)
    params = {"unit": "month", "units": "-1"}
    headers = {"Authorization": "Bearer {}".format(token)}
    response = requests.get(bitly_url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(token, url):
    bitly_url = "{0}bitlinks/{1}".format(API_URL, url)
    headers = {"Authorization": "Bearer {}".format(token)}
    response = requests.get(bitly_url, headers=headers)
    return response.ok


def main():
    load_dotenv()
    bitly_token = os.getenv('BITLY_TOKEN')
    parser = argparse.ArgumentParser(
        description=
        'Наша программа помогает посчитать кол-во кликов по ссылке. Для того чтобы получить кол-во кликов вставьте --url ссылка'
    )
    parser.add_argument('--url', help='Введите ссылку: ')
    args = parser.parse_args()
    url_parse = urlparse(args.url)
    url_without_protocol = f"{url_parse.netloc}{url_parse.path}"
    if is_bitlink(bitly_token, url_without_protocol):
        try:
            print(count_clicks(bitly_token, url_without_protocol))
        except HTTPError as error:
            print("Ошибка при подсчете кликов", error)
    else:
        try:
            print(shorten_link(bitly_token, args.url))
        except HTTPError:
            print("Неправильная ссылка: ", args.url)


if __name__ == "__main__":
    main()
