from startup import bot, botdata, botconf
from basics import *
from punch import *
from daily import *
import yaml
import datetime


with open("key.key") as rfile:
    key = rfile.read()


print("Live!")


@bot.event
async def on_ready():
    # just trying to debug here
    for guild in bot.guilds:
        for member in guild.members:
            print(member.name, ' ')

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

bot.run(key)
