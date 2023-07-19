from nextcord.ext import commands
import nextcord
import json


intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="p.", intents=intents)
