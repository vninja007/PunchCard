from init import bot
from basics import *

with open("key.key") as rfile:
    key = rfile.read()

print("Live!")
bot.run(key)
