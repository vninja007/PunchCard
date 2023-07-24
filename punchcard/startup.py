from nextcord.ext import commands
import nextcord
import yaml
import datetime

intents = nextcord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
bot = commands.Bot(command_prefix="p.", intents=intents)


with open("../config.yml", "r") as conffile:
    botconf = yaml.safe_load(conffile)

with open("../data.yml", "r") as datafile:
    botdata = yaml.safe_load(datafile)

print(type(botconf))
print(type(botdata))

timezone = botconf["timezone"]
botversion = botconf["version"]
print("Version: "+str(botversion))

offset = float(timezone[3:])
print("Offset: "+str(offset))
