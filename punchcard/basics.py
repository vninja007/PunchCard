from nextcord.ext import commands
import nextcord

import time as pytime
import datetime

from init import bot, offset, botversion


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
