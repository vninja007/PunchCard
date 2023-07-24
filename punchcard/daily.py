from nextcord.ext import commands
import nextcord
from startup import bot, botdata
from basics import writeData, writeConf, getUTime, getTime, getDate
import re
from utilfuncs import extractTime, logDates
import datetime


@bot.command()
async def wakeup(ctx, arg=""):
    ex = extractTime(arg)
    if (arg == ""):
        await ctx.send("Usage: p.wakeup [time]")
    elif (ex[0] == -1):
        await ctx.send("Incorrect time")
    else:
        logDates(ctx.author.id)
        botdata[ctx.author.id][getDate()]["wakeup"] = ":".join("0"*(2-len(str(i)))+str(i)
                                                               for i in ex)
        writeData()
        await ctx.send("Wakeup time for "+getDate()+" set to "+":".join("0"*(2-len(str(i)))+str(i)
                                                                        for i in ex))


@bot.command()
async def sleep(ctx, arg=""):
    ex = extractTime(arg)
    if (arg == ""):
        await ctx.send("Usage: p.sleep [time]")
    elif (ex[0] == -1):
        await ctx.send("Incorrect time")
    else:
        logDates(ctx.author.id)
        botdata[ctx.author.id][getDate()]["sleep"] = ":".join("0"*(2-len(str(i)))+str(i)
                                                              for i in ex)
        writeData()
        await ctx.send("Sleep time for "+getDate()+" set to "+":".join("0"*(2-len(str(i)))+str(i)
                                                                       for i in ex))


@bot.command()
async def schoolstart(ctx, arg=""):
    ex = extractTime(arg)
    if (arg == ""):
        await ctx.send("Usage: p.schoolstart [time]")
    elif (ex[0] == -1):
        await ctx.send("Incorrect time")
    else:
        logDates(ctx.author.id)
        botdata[ctx.author.id][getDate()]["schoolstart"] = ":".join("0"*(2-len(str(i)))+str(i)
                                                                    for i in ex)
        writeData()
        await ctx.send("School start time for "+getDate()+" set to "+":".join("0"*(2-len(str(i)))+str(i)
                                                                              for i in ex))


@bot.command()
async def schoolend(ctx, arg=""):
    ex = extractTime(arg)
    if (arg == ""):
        await ctx.send("Usage: p.schoolend [time]")
    elif (ex[0] == -1):
        await ctx.send("Incorrect time")
    else:
        logDates(ctx.author.id)
        botdata[ctx.author.id][getDate()]["schoolend"] = ":".join("0"*(2-len(str(i)))+str(i)
                                                                  for i in ex)
        writeData()
        await ctx.send("School end time for "+getDate()+" set to "+":".join("0"*(2-len(str(i)))+str(i)
                                                                            for i in ex))
