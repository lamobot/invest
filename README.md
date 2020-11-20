# invest

This script downloads data from yahoo finance and Tinkoff Investment API and generates the list of tickers which we can buy on MOEX or SPBEX depending on some conditions:

* share currency
* age(how many years companies pay dividends)
* company has not had a loss for several years

## Use the script

Parameters must be set:

* **token** (it should be generated on Tinkoff Invest personal account)
* **currency** (RUB, USD, EUR or ALL)
* **age** (from 1 to 20)

1. Define the token variable (bash) \
*TOKEN=your_token*

2. Run script in docker: \
*docker run lamoadm/invest:latest token=$TOKEN currency=EUR age=5* \
\
Run script in command line: \
*python3 main.py token=$TOKEN currency=EUR age=1*
