#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
from datetime import datetime
import json
from openapi_client import openapi
import yfinance as yf
import requests

# Variables
today = datetime.now().strftime("%Y-%m-%d")


def check_token(token: str) -> str:
    """Return token string"""
    if token.split('=')[0] != 'token':
        sys.exit("You must define a token")
    #if type(token.split('=')[1]) is not str:
    if not isinstance(token.split('=')[1], str):
        sys.exit("The token is incorrect")
    if "t." not in token.split('=')[1]:
        sys.exit("The token is incorrect")
    return token.split('=')[1]


def check_currency(currency: str) -> str:
    """Return currency string"""
    if currency.split('=')[0] != 'currency':
        sys.exit("You must define a currency")
    if currency.split('=')[1].strip() not in 'RUB, USD, EUR, ALL':
        sys.exit("Currency should be RUB, USD, EUR or ALL")
    return currency.split('=')[1].strip()


def check_age(age: str) -> int:
    """Return age integer"""
    age.strip()
    if age.split('=')[0] != 'age':
        sys.exit("You must define divident age")
    if not age.split('=')[1].isdigit():
        sys.exit("The age variable must be integer")
    if int(age.split('=')[1]) < 0 or int(age.split('=')[1]) > 20:
        sys.exit("The age variable must be from 1 to 20")
    return int(age.split('=')[1])


def get_ticker_list(token: str, currency: str = "ALL") -> list:
    """Return ticker list"""
    ticker_list = []
    client = openapi.api_client(token)
    try:
        stocks = client.market.market_stocks_get()
        instr_list = stocks.payload.instruments
        if currency == 'ALL':
            for instr in instr_list:
                if instr.currency == 'RUB':
                    ticker_list.append(instr.ticker + '.ME')
                if instr.currency == 'EUR':
                    ticker_list.append(instr.ticker.replace('@', '.'))
                else:
                    ticker_list.append(instr.ticker)
        elif currency == 'RUB':
            for instr in instr_list:
                if instr.currency == 'RUB':
                    ticker_list.append(instr.ticker + '.ME')
        elif currency == 'EUR':
            for instr in instr_list:
                if instr.currency == 'EUR':
                    ticker_list.append(instr.ticker.replace('@', '.'))
        elif currency == 'USD':
            for instr in instr_list:
                if instr.currency == 'USD':
                    ticker_list.append(instr.ticker)
        else:
            sys.exit("Currency should be RUB, USD, EUR or ALL")
        return ticker_list
    except:
        sys.exit('The token is incorrect test')


def get_positive_profit_list(ticker_list: list) -> list:
    """Return list with positive net profit"""
    positive_profit_list = []
    for ticker in ticker_list:
        positive_profit_list.append(ticker)
        response = requests.get("https://query1.finance.yahoo.com/v11/finance/quoteSummary/"
                                + ticker + "?modules=cashflowStatementHistory")
        if response.status_code != 404:
            quote_summary = json.loads(response.text)
            for net_income in quote_summary['quoteSummary']['result'][0] \
                ['cashflowStatementHistory']['cashflowStatements']:
                if (net_income['netIncome']['raw']) <= 0:
                    positive_profit_list.pop()
                    break
    return positive_profit_list


def get_dividends_companies(tickers: list, age: int) -> list:
    """Return list of dividends companies"""
    dividends_companies_list = []
    for ticker in tickers:
        company = yf.Ticker(ticker)
        try:
            if len(company.dividends.index.strftime('%Y').unique()) >= age:
                dividends_companies_list.append(ticker)
        except Exception:
            pass
    return dividends_companies_list


if len(sys.argv) == 4:
    lst = get_dividends_companies(
        get_positive_profit_list(get_ticker_list(check_token(sys.argv[1]),
            check_currency(sys.argv[2]))), check_age(sys.argv[3]))
    print(lst)
else:
    sys.exit("You must define all of the parameters")
