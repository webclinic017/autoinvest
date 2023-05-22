"""Module allocates pro-rated capital"""
import calendar
from datetime import datetime
import numpy as np
from credentials import trading_client, BASE_URL
from screen import tickers
from orders import buy

# account info
account = trading_client.get_account()

# trading days within a month
today = datetime.now()
last_day = f"{np.datetime64(today, 'M')}-{calendar.monthrange(today.year, today.month)[1]}"
today = np.datetime64(today, 'D')
last_day = np.datetime64(last_day)

TRADING_DAYS = np.busday_count(today, last_day)

# captial available per stock
if 'paper' in BASE_URL:
    cost_basis = 100 / float(len(tickers))
else:
    cost_basis = float(trading_client.get_account().cash) / \
        (TRADING_DAYS * float(len(tickers)))

for sym in tickers:
    buy(sym, cost_basis)