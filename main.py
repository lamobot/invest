from datetime import datetime
from openapi_client import openapi
import json
import requests

# Variables
token = ''
client = openapi.api_client(token)
today = datetime.now().strftime("%Y-%m-%d")


# Functions
def get_ticker_list(currency: str = "ALL") -> list:
    ticker_list = []
    stocks = client.market.market_stocks_get()
    instr_list = stocks.payload.instruments
    if currency == 'ALL':
        for instr in instr_list:
            if instr.currency == 'RUB':
                ticker_list.append(instr.ticker + '.ME')
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
        raise Exception('Валюта должна быть RUB, USD или EUR')
    return ticker_list

def get_positive_profit_list(ticker_list: list) -> list:
    positive_profit_list = []
    for ticker in ticker_list:
        positive_profit_list.append(ticker)
        response = requests.get("https://query1.finance.yahoo.com/v11/finance/quoteSummary/"
                                + ticker + "?modules=cashflowStatementHistory")
        if response.status_code != 404:
            quote_summary = json.loads(response.text)
            for netIncome in quote_summary['quoteSummary']['result'][0]['cashflowStatementHistory'][
                'cashflowStatements']:
                if (netIncome['netIncome']['raw']) <= 0:
                    positive_profit_list.pop()
                    break
    return positive_profit_list

def get_dividends_companies(tickers: list, age: int) -> list:
    import yfinance as yf
    dividends_companies_list = []
    for ticker in tickers:
        company = yf.Ticker(ticker)
        try:
            if len(company.dividends.index.strftime('%Y').unique()) >= age:
                dividends_companies_list.append(ticker)
        except Exception:
            pass
    return dividends_companies_list


lst = get_dividends_companies(get_positive_profit_list(get_ticker_list('EUR')), 5)
print(lst)
