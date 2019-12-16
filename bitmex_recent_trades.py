### 'education is something you don't want to finish' ###
# crushlabs@protonmail.com
# have fun, learn, give feedback

# imports
import pandas as pd 
import numpy as np 
from bitmex_websocket import BitMEXWebsocket
import datetime
import time
from time import sleep


apiKey = '' # input your api key
apiSecret = '' # input your api secret

ws = BitMEXWebsocket(endpoint="wss://www.bitmex.com/realtime",symbol='XBTUSD', api_key=apiKey, api_secret=apiSecret) # client


# socket connections
while(ws.ws.sock.connected):
    r = ws.recent_trades()
    recent = list(r[-1].items())
    ts = recent[[0][0]][1]
    sym = recent[[1][0]][1]
    side = recent[[2][0]][1]
    size = recent[[3][0]][1]
    price = recent[[4][0]][1]
    ts,sym,side,size,price
    time.sleep(3)