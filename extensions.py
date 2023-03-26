import json
import requests
from config import keys


class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(quote, base, amount):
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать вылюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать вылюту {base}')

        if quote_ticker == base_ticker:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        r = requests.get(
            f'https://api.apilayer.com/exchangerates_data/latest?symbols={quote_ticker}&base={base_ticker}')
        resp = json.loads(r.content)
        new_base = resp[quote_ticker][base_ticker] * amount
        new_base = round(new_base, 3)
        message = f'Цена {amount} {quote} в {base} : {new_base}'
        return message
