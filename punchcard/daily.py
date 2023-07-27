from nextcord.ext import commands
import nextcord
from startup import bot, botdata
from basics import writeData, writeConf, getUTime, getTime, getDate, getDateTime
import re
from utilfuncs import extractTime, logDates, correctDate
import datetime


@bot.command()
async def wakeup(ctx, *, arg=""):
    ex = getDateTime(botdata[ctx.author.id]["timezone"])
    logDates(ctx.author.id, ex, "wake")
    day = correctDate(ctx.author.id, ex, "wake")
    thedate = day.split()[0]

    botdata[ctx.author.id][thedate]["wakeup"] = ex.split()[1]
    writeData()
    await ctx.send("Wakeup time for "+str(thedate)+" set to "+ex.split()[1])


@bot.command()
async def sleep(ctx, *, arg=""):
    ex = extractTime(arg)
    if (arg == ""):
        await ctx.send("Usage: p.sleep [time]")
    elif (ex[0:2] == "-1"):
        await ctx.send("Incorrect time")
    else:
        logDates(ctx.author.id, "sleep")
        botdata[ctx.author.id][getDate()]["sleep"] = ex
        writeData()
        await ctx.send("Sleep time for "+getDate()+" set to "+ex)


@bot.command()
async def schoolstart(ctx, *, arg=""):
    ex = extractTime(arg)
    if (arg == ""):
        await ctx.send("Usage: p.schoolstart [time]")
    elif (ex[0:2] == "-1"):
        await ctx.send("Incorrect time")
    else:
        logDates(ctx.author.id, "wake")
        botdata[ctx.author.id][getDate()]["schoolstart"] = ex
        writeData()
        await ctx.send("School start time for "+getDate()+" set to "+ex)


@bot.command()
async def schoolend(ctx, *, arg=""):
    ex = extractTime(arg)
    if (arg == ""):
        await ctx.send("Usage: p.schoolend [time]")
    elif (ex[0:2] == "-1"):
        await ctx.send("Incorrect time")
    else:
        logDates(ctx.author.id, "sleep")
        botdata[ctx.author.id][getDate()]["schoolend"] = ex
        writeData()
        await ctx.send("School end time for "+getDate()+" set to "+ex)
