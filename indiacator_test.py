# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 18:56:10 2023

@author: test
"""

import numpy as np
import talib
import requests
import json
import numpy

# resLT = 'D1'  # Long-term timeframe
# resMT = 'H4'  # Medium-term timeframe

def calculate_indicator(close):
    up = np.zeros(len(close))
    dn = np.zeros(len(close))
    MTc = np.zeros(len(close))
    MTema20 = np.zeros(len(close))

    for i in range(2, len(close)):
        resLTShift = i
        resMTShift = i

        LTo = talib.EMA(close, timeperiod=2)[-resLTShift]
        LTc = talib.EMA(close, timeperiod=3)[-resLTShift]
        MTo = talib.EMA(close, timeperiod=2)[-resMTShift]
        MTc[i] = talib.EMA(close, timeperiod=3)[-resMTShift]

        LTlong = LTc > LTo
        LTshort = LTc < LTo
        MTema20[i] = talib.EMA(MTc, timeperiod=20)[-i]

        MTema20delta = MTema20[i] - MTema20[i-1]

        MTlong = MTc[i] > MTo and MTc[i] > MTema20[i] and MTema20delta > 0
        MTshort = MTc[i] < MTo and MTc[i] < MTema20[i] and MTema20delta < 0

        Long = MTlong and LTlong
        Short = MTshort and LTshort

        if Long:
            up[i] = 1
        if Short:
            dn[i] = -1

    return up, dn

a = []
OHLC = requests.get('https://min-api.cryptocompare.com/data/v2/histominute?fsym=BTC&tsym=USDT')
OHLC = json.loads(OHLC.text)
for i in OHLC["Data"]['Data']:
    a.append(i['close'])

a = numpy.array(a)
# Example usage:
# open_prices = [...]  # Replace with actual historical open prices
# high_prices = [...]  # Replace with actual historical high prices
# low_prices = [...]   # Replace with actual historical low prices
# close_prices = [...] # Replace with actual historical close prices

up, dn = calculate_indicator(a)
print("Up:", up)
print("Down:", dn)