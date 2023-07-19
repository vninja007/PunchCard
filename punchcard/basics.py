from nextcord.ext import commands
import nextcord

import time as pytime
import datetime

from init import bot, offset


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
