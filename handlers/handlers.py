from registrator import Registrator
from message import Message
from orm import *

@Registrator(key="error")
async def error_handler(message: Message):
    await message.send_answer('Вы отправили незарегистрированную команду')
#Registrator.register(key='error', handler=error_handler)

@Registrator(key="/start")
async def start_handler(message: Message):
    await message.send_answer('сам ты '+message.text)
# Registrator.register(key='/start', handler=start_handler)

#@Registrator(key="/hello")
async def hello_handler(message: Message):
    await message.send_answer('Привет, юзер '+ str(message.user))
Registrator.register(key='/hello', handler=hello_handler)
