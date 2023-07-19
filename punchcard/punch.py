from nextcord.ext import commands
import nextcord
from startup import bot, botdata
from basics import writeData, writeConf, getUTime, getTime


@bot.command()
async def init(ctx, arg=""):
    print(type(botdata))
    if (ctx.author.id not in botdata):

        botdata[ctx.author.id] = {}
        botdata[ctx.author.id]["total"] = 0
        botdata[ctx.author.id]["sessions"] = 0
        botdata[ctx.author.id]["start"] = -1
        writeData()
        await ctx.send("Initialized user. You now exist! Use p.start and p.stop for check-in/check-out!")
    else:
        await ctx.send("User already exists!")


@bot.command()
async def start(ctx, arg=""):
    if (ctx.author.id in botdata):
        if (botdata[ctx.author.id]["start"] == -1):
            ut = getUTime()
            tt = getTime()
            botdata[ctx.author.id]["start"] = getUTime()
            writeData()
            await ctx.send("Clocked in at " + str(tt))
        else:
            await ctx.send("User is already clocked in! Use p.stop to clock out!")
    else:
        await ctx.send("User does not exist! Type p.init to begin!")


@bot.command()
async def stop(ctx, arg=""):
    if (ctx.author.id in botdata):
        if (botdata[ctx.author.id]["start"] != -1):
            ut = getUTime()
            tt = getTime()
            t1 = botdata[ctx.author.id]["start"]
            t2 = getUTime()
            worked = round((t2-t1)/60, 2)
            hrs = (t2-t1)//3600
            mins = ((t2-t1)//60) % 60
            secs = ((t2-t1) % 60) // 1
            botdata[ctx.author.id]["total"] += worked
            botdata[ctx.author.id]["start"] = -1
            writeData()
            await ctx.send("Clocked out at " + str(tt) + ". You worked for "+str(hrs)+" hrs "+str(mins)+" mins "+str(secs)+".")
        else:
            await ctx.send("User is already clocked out! Use p.start to clock in!")
    else:
        await ctx.send("User does not exist! Type p.init to begin!")
