from nextcord.ext import commands
import nextcord
from startup import bot, botdata
from basics import writeData, writeConf, getUTime, getTime, getDate, getDateTime
import re
from utilfuncs import extractTime, logDates, correctDate, addDaytoDate, diffTimefromTime
import datetime


@bot.command()
async def wakeup(ctx, *, arg=""):
    if (ctx.author.id in botdata):
        ex = getDateTime(botdata[ctx.author.id]["timezone"])
        logDates(ctx.author.id, ex, "wake")
        day = correctDate(ctx.author.id, ex, "wake")
        thedate = day.split()[0]

        botdata[ctx.author.id][thedate]["wakeup"] = ex.split()[1]
        botdata[ctx.author.id]["status"] = "free"

        yesterday = addDaytoDate(thedate, -1)
        yesterday = yesterday.split()[0]
        print(yesterday)
        if (yesterday in botdata[ctx.author.id]):
            if ("sleep" in botdata[ctx.author.id][yesterday]):
                sleeptime = diffTimefromTime(
                    botdata[ctx.author.id][yesterday]["sleep"], botdata[ctx.author.id][thedate]["wakeup"])
                botdata[ctx.author.id][thedate]["sleeptime"] = str(sleeptime)
        writeData()
        await ctx.send("Wakeup time for "+str(thedate)+" set to "+ex.split()[1])
    else:
        await ctx.send("User does not exist! Type p.init to begin!")


@bot.command()
async def sleep(ctx, *, arg=""):
    if (ctx.author.id in botdata):
        ex = getDateTime(botdata[ctx.author.id]["timezone"])
        logDates(ctx.author.id, ex, "sleep")
        day = correctDate(ctx.author.id, ex, "sleep")
        thedate = day.split()[0]

        botdata[ctx.author.id][thedate]["sleep"] = ex.split()[1]
        botdata[ctx.author.id]["status"] = "sleeping"

        tomorrow = addDaytoDate(thedate, 1)
        tomorrow = tomorrow.split()[0]
        print(tomorrow)
        if (tomorrow in botdata[ctx.author.id]):
            if ("wakeup" in botdata[ctx.author.id][tomorrow]):
                sleeptime = diffTimefromTime(
                    botdata[ctx.author.id][thedate]["sleep"], botdata[ctx.author.id][tomorrow]["wakeup"])
                botdata[ctx.author.id][tomorrow]["sleeptime"] = str(sleeptime)
        writeData()
        await ctx.send("Sleep time for "+str(thedate)+" set to "+ex.split()[1])
    else:
        await ctx.send("User does not exist! Type p.init to begin!")


@bot.command()
async def schoolstart(ctx, *, arg=""):
    if (ctx.author.id in botdata):
        ex = getDateTime(botdata[ctx.author.id]["timezone"])
        logDates(ctx.author.id, ex, "schoolstart")
        day = correctDate(ctx.author.id, ex, "schoolstart")
        thedate = day.split()[0]

        botdata[ctx.author.id][thedate]["schoolstart"] = ex.split()[1]
        botdata[ctx.author.id]["status"] = "school"

        print(thedate)
        if (thedate in botdata[ctx.author.id]):
            if ("schoolend" in botdata[ctx.author.id][thedate]):
                schooltime = diffTimefromTime(
                    botdata[ctx.author.id][thedate]["schoolstart"], botdata[ctx.author.id][thedate]["schoolend"])
                botdata[ctx.author.id][thedate]["schooltime"] = str(
                    schooltime)
        writeData()
        await ctx.send("School start time for "+str(thedate)+" set to "+ex.split()[1])
    else:
        await ctx.send("User does not exist! Type p.init to begin!")


@bot.command()
async def schoolend(ctx, *, arg=""):
    if (ctx.author.id in botdata):
        ex = getDateTime(botdata[ctx.author.id]["timezone"])
        logDates(ctx.author.id, ex, "schoolend")
        day = correctDate(ctx.author.id, ex, "schoolend")
        thedate = day.split()[0]

        botdata[ctx.author.id][thedate]["schoolend"] = ex.split()[1]
        botdata[ctx.author.id]["status"] = "free"

        print(thedate)
        if (thedate in botdata[ctx.author.id]):
            if ("schoolstart" in botdata[ctx.author.id][thedate]):
                schooltime = diffTimefromTime(
                    botdata[ctx.author.id][thedate]["schoolstart"], botdata[ctx.author.id][thedate]["schoolend"])
                botdata[ctx.author.id][thedate]["schooltime"] = str(
                    schooltime)
        writeData()
        await ctx.send("School end time for "+str(thedate)+" set to "+ex.split()[1])
    else:
        await ctx.send("User does not exist! Type p.init to begin!")


@bot.command()
async def reset(ctx, *, arg=""):
    if (ctx.author.id in botdata):
        if (arg not in ["schoolend", "schoolstart", "wakeup", "wake", "sleep"]):
            await ctx.send("Improper command")
        else:
            try:
                arg = arg.replace("up", "")
                arg = arg.replace("wake", "wakeup")
                del botdata[ctx.author.id][arg]
                arg = arg.replace("school", "school ")
                await ctx.send(f"Reset {arg}. It is not logged anymore.")
            except KeyError:
                arg = arg.replace("up", "")
                arg = arg.replace("wake", "wakeup")
                arg = arg.replace("school", "school ")
                arg = arg[0].upper() + arg[1:]
                await ctx.send(f"{arg} is not defined for today")
    else:
        await ctx.send("User does not exist! Type p.init to begin!")
