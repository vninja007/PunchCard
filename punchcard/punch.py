from nextcord.ext import commands
import nextcord
from startup import bot, botdata
from basics import writeData, writeConf


@bot.command()
async def init(ctx, arg=""):
    print(type(botdata))
    if (ctx.author.id not in botdata):

        botdata[ctx.author.id] = {}
        botdata[ctx.author.id]["total"] = 0
        botdata[ctx.author.id]["sessions"] = 0
        writeData()
        await ctx.send("Initialized user. You now exist! Use p.start and p.stop for check-in/check-out!")
    else:
        await ctx.send("User already exists!")
