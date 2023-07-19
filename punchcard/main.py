from startup import bot, botdata, botconf
from basics import *
from punch import *
import yaml
import datetime


with open("key.key") as rfile:
    key = rfile.read()

print("Live!")
bot.run(key)
