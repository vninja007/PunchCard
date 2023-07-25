from nextcord.ext import commands
import nextcord

import time as pytime
import datetime
import yaml

from startup import bot, offset, botversion, botdata, botconf


@bot.command()
async def getId(ctx, arg=""):
    await ctx.send("<@"+str(ctx.author.id)+">")


@bot.command()
async def echo(ctx, arg="ㅤ"):
    await ctx.send(arg)


@bot.command()
async def foo(ctx, arg=1):
    await ctx.send("bar")


@bot.command()
async def utime(ctx, arg=""):
    await ctx.send(str(pytime.time() - 3600*offset))


@bot.command()
async def time(ctx, arg=""):
    dtn = datetime.datetime.now() - datetime.timedelta(hours=offset)
    dt = str(dtn)
    dt = dt[:dt.index(".")]
    await ctx.send(dt)


def getTime(useroffset=0):
    dtn = datetime.datetime.now() - datetime.timedelta(hours=offset) + \
        datetime.timedelta(hours=useroffset)
    dt = str(dtn)
    dt = dt[:dt.index(".")]
    return dt


def getDate(arg=""):
    dtn = datetime.datetime.now() - datetime.timedelta(hours=offset)
    dt = str(dtn)
    dt = dt[:dt.index(" ")]
    return dt


def getDateTime():
    dtn = datetime.datetime.now() - datetime.timedelta(hours=offset)
    dt = str(dtn.strftime("%Y-%m-%d %H:%M:%S"))
    return dt


def getUTime(arg=""):
    return (pytime.time() - 3600*offset)


@bot.command()
async def version(ctx, arg=""):
    await ctx.send(botversion)


@bot.command()
async def ping(ctx, arg=""):
    p1 = ctx.message.created_at.replace(tzinfo=None)
    p2 = datetime.datetime.now().replace(tzinfo=None) - \
        datetime.timedelta(hours=offset)
    diff = str(p2-p1)
    difftime = round(float(diff[diff.index("."):])*1000)

    await ctx.send("Pong! "+str(difftime)+" ms")


def writeData():
    with open("../data.yml", "w+") as wfile:
        botdata["timestamp"] = getTime()
        yaml.dump(botdata, wfile)


def writeConf():
    with open("../conf.yml", "w+") as wfile:
        yaml.dump(botconf, wfile)
