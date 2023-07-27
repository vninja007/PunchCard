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
    botdata[ctx.author.id]["status"] = "free"
    writeData()
    await ctx.send("Wakeup time for "+str(thedate)+" set to "+ex.split()[1])


@bot.command()
async def sleep(ctx, *, arg=""):
    ex = getDateTime(botdata[ctx.author.id]["timezone"])
    logDates(ctx.author.id, ex, "sleep")
    day = correctDate(ctx.author.id, ex, "sleep")
    thedate = day.split()[0]

    botdata[ctx.author.id][thedate]["sleep"] = ex.split()[1]
    botdata[ctx.author.id]["status"] = "sleeping"
    writeData()
    await ctx.send("Sleep time for "+str(thedate)+" set to "+ex.split()[1])


@bot.command()
async def schoolstart(ctx, *, arg=""):
    ex = getDateTime(botdata[ctx.author.id]["timezone"])
    logDates(ctx.author.id, ex, "wake")
    day = correctDate(ctx.author.id, ex, "wake")
    thedate = day.split()[0]

    botdata[ctx.author.id][thedate]["schoolstart"] = ex.split()[1]
    botdata[ctx.author.id]["status"] = "school"
    writeData()
    await ctx.send("School start time for "+str(thedate)+" set to "+ex.split()[1])


@bot.command()
async def schoolend(ctx, *, arg=""):
    ex = getDateTime(botdata[ctx.author.id]["timezone"])
    logDates(ctx.author.id, ex, "sleep")
    day = correctDate(ctx.author.id, ex, "sleep")
    thedate = day.split()[0]

    botdata[ctx.author.id][thedate]["schoolend"] = ex.split()[1]
    botdata[ctx.author.id]["status"] = "free"
    writeData()
    await ctx.send("School end time for "+str(thedate)+" set to "+ex.split()[1])
