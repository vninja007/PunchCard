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
        botdata[ctx.author.id]["livetask"] = ""
        botdata[ctx.author.id]["tasks"] = {}
        writeData()
        await ctx.send("Initialized user. You now exist! Use p.start and p.stop for check-in/check-out!")
    else:
        await ctx.send("User already exists!")


@bot.command()
async def maketask(ctx, *, arg=""):
    arg = arg.lower()
    if (ctx.author.id in botdata):
        if (arg == ""):
            await ctx.send("No task specified. Usage: p.maketask [task]")

        else:
            if (arg in botdata[ctx.author.id]["tasks"]):
                await ctx.send("Task already exists")
            else:
                botdata[ctx.author.id]["tasks"][arg] = 0.0
                await ctx.send("Created task '"+arg+"'")
                writeData()
    else:
        await ctx.send("User does not exist! Type p.init to begin!")


@bot.command()
async def deltask(ctx, *, arg=""):
    arg = arg.lower()
    if (ctx.author.id in botdata):
        if (arg == ""):
            await ctx.send("No task specified. Usage: p.deltask [task]")

        else:
            if (arg not in botdata[ctx.author.id]["tasks"]):
                await ctx.send("Task does not exist!")
            else:
                del botdata[ctx.author.id]["tasks"][arg]
                await ctx.send("Deleted task '"+arg+"'")
                writeData()
    else:
        await ctx.send("User does not exist! Type p.init to begin!")


@bot.command()
async def start(ctx, *, arg=""):
    arg = arg.lower()
    if (ctx.author.id in botdata):
        if (botdata[ctx.author.id]["start"] == -1):
            if (arg != ""):
                if (arg not in botdata[ctx.author.id]["tasks"]):
                    await ctx.send("No task named '"+arg+"'")
                else:
                    ut = getUTime()
                    tt = getTime()
                    botdata[ctx.author.id]["start"] = getUTime()
                    botdata[ctx.author.id]["livetask"] = arg
                    writeData()
                    await ctx.send("Clocked in for '"+arg+"' at " + str(tt))
            else:
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
async def stop(ctx, *, arg=""):
    arg = arg.lower()
    if (ctx.author.id in botdata):
        if (botdata[ctx.author.id]["start"] != -1):
            ut = getUTime()
            tt = getTime()
            t1 = botdata[ctx.author.id]["start"]
            t2 = getUTime()
            worked = float('{0:.2f}'.format((t2-t1)/60))
            hrs = (t2-t1)//3600
            mins = ((t2-t1)//60) % 60
            secs = ((t2-t1) % 60) // 1
            if (botdata[ctx.author.id]["livetask"] != ""):
                task = botdata[ctx.author.id]["livetask"]
                botdata[ctx.author.id]["tasks"][task] += worked
                botdata[ctx.author.id]["livetask"] = ""
                botdata[ctx.author.id]["total"] += worked
                botdata[ctx.author.id]["start"] = -1
                botdata[ctx.author.id]["sessions"] += 1
                writeData()
                await ctx.send("Clocked out from '"+arg+"' at " + str(tt) + ". You worked for "+str(int(hrs))+" hrs "+str(int(mins))+" mins "+str(int(secs))+" secs.")
            else:
                botdata[ctx.author.id]["total"] += worked
                botdata[ctx.author.id]["start"] = -1
                botdata[ctx.author.id]["sessions"] += 1
                writeData()
                await ctx.send("Clocked out at " + str(tt) + ". You worked for "+str(int(hrs))+" hrs "+str(int(mins))+" mins "+str(int(secs))+" secs.")
        else:
            await ctx.send("User is already clocked out! Use p.start to clock in!")
    else:
        await ctx.send("User does not exist! Type p.init to begin!")
