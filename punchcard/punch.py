from nextcord.ext import commands
import nextcord
from startup import bot, botdata
from basics import writeData, writeConf, getUTime, getTime, getDateTime, getDate
from utilfuncs import clockOutProcedure, addDaytoDate, correctDate, checkTimeSpent, getProductivity, getDayProductivity


@bot.command()
async def init(ctx, arg=""):
    arg = arg.upper()
    arg = arg.replace("UTC", "")
    arg = arg.replace("GMT", "")
    arg = arg.replace("+", "")
    if (ctx.author.id not in botdata):
        if (arg != "" or not arg.isnumeric()):
            botdata[ctx.author.id] = {}
            botdata[ctx.author.id]["total"] = "00:00:00"
            botdata[ctx.author.id]["sessions"] = 0
            botdata[ctx.author.id]["timezone"] = int(arg)
            botdata[ctx.author.id]["status"] = "free"
            botdata[ctx.author.id]["sessionslist"] = {}
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
async def status(ctx, arg=""):
    if (ctx.author.id in botdata):
        await ctx.send("You are "+botdata[ctx.author.id]["status"])
    else:
        await ctx.send("User does not exist! Type p.init to begin!")


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
    elif (botdata[ctx.author.id]["status"] == "sleeping"):
        await ctx.send("You are sleeping! Use p.wakeup to wake up!")
    elif (botdata[ctx.author.id]["status"] == "school"):
        await ctx.send("You are in school! Use p.schoolend (Note: school hours are auto-included in productivity calculations)")
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
                        botdata[ctx.author.id]["status"] = "working"
                        ex = getDateTime(botdata[ctx.author.id]["timezone"])
                        day = correctDate(ctx.author.id, ex, "wake")
                        thedate = day.split()[0]
                        print(thedate)
                        if ("wakeup" not in botdata[ctx.author.id][thedate]):
                            botdata[ctx.author.id][thedate]["wakeup"] = str(tt)
                            await ctx.send("Automatically set wakeup time for "+str(thedate)+" to "+str(tt))
                        writeData()
                        await ctx.send("Clocked in for '"+arg+"' at " + str(tt))
                else:
                    ut = getUTime()
                    tt = getTime(botdata[ctx.author.id]["timezone"])
                    botdata[ctx.author.id]["start"] = getDateTime()
                    botdata[ctx.author.id]["status"] = "working"
                    ex = getDateTime(botdata[ctx.author.id]["timezone"])
                    day = correctDate(ctx.author.id, ex, "wake")
                    thedate = day.split()[0]
                    print(thedate)
                    if ("wakeup" not in botdata[ctx.author.id][thedate]):
                        botdata[ctx.author.id][thedate]["wakeup"] = str(tt)
                        await ctx.send("Automatically set wakeup time for "+str(thedate)+" to "+str(tt))
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
            starttime = botdata[ctx.author.id]["start"]
            endtime = getTime()
            tog = botdata[ctx.author.id]["livetask"] if "livetask" in botdata[ctx.author.id] else ""
            tt, hms = clockOutProcedure(ctx.author.id)
            if (tog != ""):
                print("true")
                botdata[ctx.author.id]["sessionslist"][botdata[ctx.author.id]
                                                       ["sessions"]] = [starttime, endtime, tog]

            else:
                botdata[ctx.author.id]["sessionslist"][botdata[ctx.author.id]
                                                       ["sessions"]] = [starttime, endtime]
            print(botdata[ctx.author.id]["sessionslist"]
                  [botdata[ctx.author.id]["sessions"]])
            writeData()
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
        if (after.id in botdata):
            if ("start" in botdata[after.id]):
                tt, hms = clockOutProcedure(after.id)
                user = await bot.fetch_user(after.id)
                await user.send("You have been clocked out due to closing discord"+". You worked for "+str(hms))


@bot.command()
async def tasklist(ctx, arg=""):
    if (ctx.author.id in botdata):
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
    else:
        await ctx.send("User does not exist! Type p.init to begin!")


def elapsedError():
    s = """Malformed argument! Use one of the following:
    p.elapsed
    p.elapsed [task]
    p.elapsed [YYYY-MM-DD] [YYYY-MM-DD]
    p.elapsed [task] [YYYY-MM-DD] [YYYY-MM-DD]
    p.elapsed [YYYY-MM-DD HH:mm:SS] [YYYY-MM-DD HH:mm:SS]
    p.elapsed [task] [YYYY-MM-DD HH:mm:SS] [YYYY-MM-DD HH:mm:SS]"""
    return s


@bot.command()
async def elapsed(ctx, *, arg=""):
    if (arg == ""):
        timespent = checkTimeSpent(ctx.author.id, "1000-01-01", "9999-01-01")
        await ctx.send(f"You have worked for {timespent}, excluding school hours")
    else:
        arg = arg.split()
        if (len(arg) == 1):
            task = arg[0]
            timespent = checkTimeSpent(
                ctx.author.id, "1000-01-01", "9999-01-01", task)
            await ctx.send(f"You have worked on {task} for {timespent}, excluding school hours")
        elif (len(arg) == 2):
            st = arg[0]
            et = arg[1]
            try:
                await ctx.send(f"You have worked for {checkTimeSpent(ctx.author.id, st, et)}, excluding school hours")
            except ValueError:
                await ctx.send(elapsedError())
        elif (len(arg) == 3):
            task = arg[0]
            st = arg[1]
            et = arg[2]
            try:
                await ctx.send(f"You have worked on {task} for {checkTimeSpent(ctx.author.id, st, et, task)}, excluding school hours")

            except ValueError:
                await ctx.send(elapsedError())
        elif (len(arg) == 4):
            st = arg[0]
            sh = arg[1]
            et = arg[2]
            eh = arg[3]

            try:
                await ctx.send(f"You have worked for {checkTimeSpent(ctx.author.id, st+' '+sh, et+' '+eh)}, excluding school hours")

            except ValueError:
                await ctx.send(elapsedError())
        elif (len(arg) == 5):
            task = arg[0]
            st = arg[1]
            sh = arg[2]
            et = arg[3]
            eh = arg[4]
            try:
                await ctx.send(f"You have worked on {task} for {checkTimeSpent(ctx.author.id, st+' '+sh, et+' '+eh, task)}, excluding school hours")

            except ValueError:
                await ctx.send(elapsedError())
        else:
            await ctx.send(elapsedError())


def prodError():
    s = """Malformed argument! Use one of the following:
    p.productivity YYYY-MM-DD YYYY-MM-DD
    p.productivity YYYY-MM-DD HH:mm:SS HH:mm:SS
    p.productivity YYYY-MM-DD HH:mm:SS YYYY-MM-DD HH:mm:SS
    p.dayproductivity YYYY-MM-DD
    """
    return s

# Accurate to 3 decimal places because...


@bot.command()
async def productivity(ctx, *, arg=""):
    arg = arg.split()
    if (not (1 <= len(arg) <= 4)):
        await ctx.send(prodError())
    else:
        if (len(arg) == 1):
            arg = [arg[0], "00:00:00", arg[0], "11:59:59"]
        elif (len(arg) == 2):
            arg = [arg[0], "00:00:00", arg[1], "11:59:59"]
        elif (len(arg) == 3):
            arg = [arg[0], arg[1], arg[0], arg[2]]
        else:  # len(arg)==4
            pass
        try:
            prod = float(getProductivity(
                ctx.author.id, arg[0]+" "+arg[1], arg[2]+" "+arg[3]))
            prod = round(1000*prod)/10
            await ctx.send(f"Productivity for {arg[0]} {arg[1]} to {arg[2]} {arg[3]} was **{prod}%**")
        except (IndexError, ValueError):
            await ctx.send(prodError())
