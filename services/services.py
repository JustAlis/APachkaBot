#async services for some background work
#check message.py for reference

import asyncio
import requests
from registrator import ServiceRegistrator
from orm import *
from config import HEADERS_AUTH, MESSEGE_URL


@ServiceRegistrator
async def test_interval():
    while True:
        print('echo')
        await asyncio.sleep(5)
# ServiceRegistrator.register(test_interval)

#@ServiceRegistrator
async def timer():
    x = 1
    while True:
        print(x)
        x+=1
        await asyncio.sleep(1)
ServiceRegistrator.register(timer)

