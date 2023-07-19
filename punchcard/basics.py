from nextcord.ext import commands
import nextcord
import time as pytime
import datetime
from init import bot


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
    await ctx.send(str(pytime.time()))


@bot.command()
async def time(ctx, arg=""):
    dt = str(datetime.datetime.now())
    dt = dt[:dt.index(".")]
    await ctx.send(dt)
