from typing import List

from bs4 import BeautifulSoup
import requests

from parsers.bank import Bank


class KiGroupParser(Bank):
    __URL = 'https://www.fbank.com.ua/'
    __BANK_NAME = 'FBank'

    def __init__(self, currencies: List, bank_url: str, bank_id: int):
        self.__currencies = {
            element[2]: (element[0], element[1]) for element in currencies
        }
        self.__bank_url = bank_url
        self.__bank_id = bank_id

    def __get_html(self):
        resp = requests.get(self.__bank_url)
        return resp.text

    def get_currency_rate(self):
        currency_rate = {
            'bank_id': self.__bank_id,
            'rate': []
        }

        html = self.__get_html()
        soup = BeautifulSoup(html, 'lxml')

        contents = soup.find('table').find('tr').find_all('td', {'class': 'bg_grey'})
        lst = []
        for line in contents:
            lst.append(line.text)
        currency_id = [1,2,3]
        purchase = []
        purchase.append(lst[1])
        purchase.append(lst[5])
        purchase.append(lst[9])
        sale = []
        sale.append(lst[2])
        sale.append(lst[6])
        sale.append(lst[10])
        currency_rate['rate'].append(
                {
                    'currency_id': currency_id,
                    'purchase': purchase,
                    'sale': sale
                }
            )

        return currency_rate


if __name__ == '__main__':
    from connector import DbUtils
    from pprint import pprint

    db = DbUtils()
    db.connect()
    currencies = db.get_currencies()
    bank_id, bank_name, bank_url = db.get_bank_by_id(7)
    db.close()
    parser = KiGroupParser(currencies, bank_url, bank_id)
    pprint(parser.get_currency_rate())
























