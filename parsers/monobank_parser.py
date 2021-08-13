from typing import List
from typing import List
import requests

from parsers.bank import Bank


class MonobankParser(Bank):
    def __init__(self, currencies: List, bank_url: str, bank_id: int):
        self.__currencies = {
            element[2]: (element[0], element[1]) for element in currencies
        }
        self.__bank_url = bank_url
        self.__bank_id = bank_id

    def __get_json(self):
        resp = requests.get(self.__bank_url)
        return resp.json()

    def get_currency_rate(self):
        currency_rate = {
            'bank_id': self.__bank_id,
            'rate': []
        }

        result = self.__get_json()
        count = 0
        for line in result in round[:3]:
            #if line['currencyCodeA'].strip().lower() in self.__currencies.keys():
            # currency_id = 1
            # currency_id +=1

            # for key, value in self.__currencies.items():
            #     if key.lower() in line['id'].lower():
            #         currency_id = value[0]


            currency_rate['rate'].append(
                 {
                         'currency_id': currency_id,
                         'purchase': round(float(line['rateBuy']), 2),
                         'sale': round(float(line['rateSell']), 2)
                }
                )

        return currency_rate


if __name__ == '__main__':
    from connector import DbUtils
    from pprint import pprint

    db = DbUtils()
    db.connect()
    currencies = db.get_currencies()
    bank_id, bank_name, bank_url = db.get_bank_by_id(6)
    db.close()
    parser = MonobankParser(currencies, bank_url, bank_id)
    pprint(parser.get_currency_rate())