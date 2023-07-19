from nextcord.ext import commands
import nextcord
import yaml


intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="p.", intents=intents)

with open("../config.yml", "r") as conffile:
    botconf = yaml.safe_load(conffile)

with open("../data.yml", "r") as datafile:
    botdata = yaml.safe_load(datafile)

timezone = botconf["Timezone"]
offset = float(timezone[3:])
print("Offset: "+str(offset))
