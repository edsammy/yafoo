#!/usr/bin/env python3
import re
import requests
import json
from helpers import get_today_timestamp, get_year_timestamp, more_than_one_line, str_data_to_dict, sort_by_date

_cookie = None
_crumb = None

def get_cookie_crumb():
    # cookie and crumb for yahoo finance v7
    # http://blog.bradlucas.com/posts/2017-06-03-yahoo-finance-quote-download-python/
    global _cookie
    global _crumb

    # only get cookie crumb if we dont have one from a previous request
    if _cookie == None and _crumb == None:
        # make a dummy request to get a cookie & crumb for future requests 
        dummy_request = requests.get("https://finance.yahoo.com/quote/QCOM")
        _cookie = {'B':dummy_request.cookies['B']}

        # good regex explaination https://stackoverflow.com/questions/9889635/regular-expression-to-return-all-characters-between-two-special-characters
        raw_crumb = re.findall('"CrumbStore":{"crumb":"(.*?)"', dummy_request.text)[0]
        # replace unicode \u002F with forward slash
        _crumb = re.sub(r'\\u002F','/',raw_crumb)

def get_dividend_history(sym):
    get_cookie_crumb()
    # starting period = 1/2/1962
    download = requests.get(
        'https://query1.finance.yahoo.com/v7/finance/download/' + sym +
        '?period1=-252345600' + '&period2=' + str(get_today_timestamp()) +
        '&interval=1d&events=div&crumb=' + _crumb, cookies = _cookie
        )
    
    if more_than_one_line(download.text):
        data = str_data_to_dict(download.text)
        data = sort_by_date(data)
        return data
    else:
        return -1

def get_price_history(sym):
    get_cookie_crumb()
    # starting period = 1/2/1962
    download = requests.get(
        'https://query1.finance.yahoo.com/v7/finance/download/' + sym +
        '?period1=-252345600' + '&period2=' + str(get_today_timestamp()) +
        '&interval=1d&events=history&crumb=' + _crumb, cookies = _cookie
        )

    if more_than_one_line(download.text):
        data = str_data_to_dict(download.text)
        return data
    else:
        return -1

def get_price_history_on(sym, date):
    return list(filter(lambda x: x['Date'] == date, get_price_history(sym)))[0]
    
def get_quote(sym):
    # api calls: https://github.com/herval/yahoo-finance/issues/51
    download = requests.get(
        'https://query1.finance.yahoo.com/v7/finance/quote?symbols=' + sym
        )
    response = download.json()['quoteResponse']['result']
    try:
        if len(response) > 0:
            response = response[0]
            if response['tradeable']:
                # lots of random strings exist but arent tradeable
                return response
            else:
                return -1
        else:
            return -1
    except:
        # got a NoneType response once?
        return -1

def has_current_dividend(sym):
    quote = get_quote(sym)
    if quote == -1:
        return -1
    else:
        if 'dividendDate' in quote:
            next_dividend_date = quote['dividendDate']
            if next_dividend_date >= get_year_timestamp():
                return 1
            else:
                return 0
        else:
            return 0