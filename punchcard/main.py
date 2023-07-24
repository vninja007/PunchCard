from startup import bot, botdata, botconf
from basics import *
from punch import *
from daily import *
import yaml
import datetime
import asyncio


with open("key.key") as rfile:
    key = rfile.read()


print("Live!")
bot.run(key)
