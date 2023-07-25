from nextcord.ext import commands
import nextcord
from startup import bot, botdata
from basics import writeData, writeConf, getUTime, getTime, getDateTime
from utilfuncs import clockOutProcedure


@bot.command()
async def init(ctx, arg=""):
    arg = arg.upper()
    arg = arg.replace("UTC", "")
    arg = arg.replace("GMT", "")
    arg = arg.replace("+", "")
    print(type(botdata))
    if (ctx.author.id not in botdata):
        if (arg != "" or not arg.isnumeric()):
            botdata[ctx.author.id] = {}
            botdata[ctx.author.id]["total"] = "00:00:00"
            botdata[ctx.author.id]["sessions"] = 0
            botdata[ctx.author.id]["timezone"] = int(arg)
            # botdata[ctx.author.id]["start"] = -1
            # botdata[ctx.author.id]["livetask"] = ""
            botdata[ctx.author.id]["tasks"] = {}
            writeData()
            await ctx.send("Initialized user. You now exist! Use p.start and p.stop for check-in/check-out!")
        else:
            await ctx.send("Usage: p.init (timezone)")
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
                botdata[ctx.author.id]["tasks"][arg] = "00:00:00"
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
    if (ctx.message.author.raw_status == "offline"):
        await ctx.send("You are offline/invisible! Please change to online/idle/donotdisturb to start!")

    else:
        arg = arg.lower()
        if (ctx.author.id in botdata):
            if ("start" not in botdata[ctx.author.id]):
                if (arg != ""):
                    if (arg not in botdata[ctx.author.id]["tasks"]):
                        await ctx.send("No task named '"+arg+"'")
                    else:
                        ut = getUTime()
                        tt = getTime(botdata[ctx.author.id]["timezone"])
                        botdata[ctx.author.id]["start"] = getDateTime()
                        botdata[ctx.author.id]["livetask"] = arg
                        writeData()
                        await ctx.send("Clocked in for '"+arg+"' at " + str(tt))
                else:
                    ut = getUTime()
                    tt = getTime(botdata[ctx.author.id]["timezone"])
                    botdata[ctx.author.id]["start"] = getDateTime()
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
        if ("start" in botdata[ctx.author.id]):
            tt, hms = clockOutProcedure(ctx.author.id)
            if (arg != ""):
                await ctx.send("Clocked out from '"+arg+"' at " + str(tt) + ". You worked for "+str(hms))
            else:
                await ctx.send("Clocked out at " + str(tt) + ". You worked for "+str(hms))

        else:
            await ctx.send("User is already clocked out! Use p.start to clock in!")
    else:
        await ctx.send("User does not exist! Type p.init to begin!")


@bot.event
async def on_presence_update(before, after):
    if str(after.status) == "offline":
        print("{} has gone {}.".format(after.name, after.status))
        if (after.id in botdata):
            if ("start" in botdata[after.id]):
                tt, hms = clockOutProcedure(after.id)
                user = await bot.fetch_user(after.id)
                await user.send("You have been clocked out due to closing discord"+". You worked for "+str(hms))


@bot.command()
async def tasklist(ctx, arg=""):
    if (len(botdata[ctx.author.id]["tasks"]) == 0):
        await ctx.send("No tasks logged")
    else:
        tosend = ""
        runtot = 0.0
        for i in botdata[ctx.author.id]["tasks"]:
            tosend += i
            runtot += botdata[ctx.author.id]["tasks"][i]
            hrs = (botdata[ctx.author.id]["tasks"][i])//60
            mins = int(botdata[ctx.author.id]["tasks"][i]//1)
            secs = (botdata[ctx.author.id]["tasks"][i] * 60) // 1
            hrs = int(hrs)
            mins = int(mins)
            secs = int(secs)
            hrs = str(hrs) if hrs >= 10 else "0"+str(hrs)
            mins = str(mins) if mins >= 10 else "0"+str(mins)
            secs = str(secs) if secs >= 10 else "0"+str(secs)
            tosend += ": "+hrs+":"+mins+":"+secs+"\n"
        leftovers = botdata[ctx.author.id]["total"]-runtot
        hrs = (leftovers)//60
        mins = int(leftovers//1)
        secs = (leftovers * 60) // 1
        hrs = int(hrs)
        mins = int(mins)
        secs = int(secs)
        hrs = str(hrs) if hrs >= 10 else "0"+str(hrs)
        mins = str(mins) if mins >= 10 else "0"+str(mins)
        secs = str(secs) if secs >= 10 else "0"+str(secs)
        tosend += "UNASSIGNED: "+hrs+":"+mins+":"+secs+"\n"
        tosend += "-"*40
        hrs = (botdata[ctx.author.id]["total"])//60
        mins = int(botdata[ctx.author.id]["total"]//1)
        secs = (botdata[ctx.author.id]["total"] * 60) // 1
        hrs = int(hrs)
        mins = int(mins)
        secs = int(secs)
        hrs = str(hrs) if hrs >= 10 else "0"+str(hrs)
        mins = str(mins) if mins >= 10 else "0"+str(mins)
        secs = str(secs) if secs >= 10 else "0"+str(secs)
        tosend += "\nTotal: "+hrs+":"+mins+":"+secs+"\n"
        await ctx.send(tosend)
