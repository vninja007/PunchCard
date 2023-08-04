import re
import datetime
from basics import getDate
from startup import botdata, botconf
from basics import writeData, getUTime, getTime, getDateTime
from datetime import time as dtime
from datetime import date, timedelta
from datetime import datetime

"""
Procedure for clocking out
"""


def clockOutProcedure(author):
    t1 = botdata[author]["start"]               # 2023-01-01 12:34:56
    t2 = getDateTime()                          # 2023-01-01 13:34:56
    tt = getTime(botdata[author]["timezone"])
    elapsed = diffDatefromDate(t1, t2)   # 01:00:00
    if ("livetask" in botdata[author]):

        task = botdata[author]["livetask"]
        botdata[author]["tasks"][task] = addTimetoTime(
            elapsed, botdata[author]["tasks"][task])
        del botdata[author]["livetask"]
        botdata[author]["total"] = addTimetoTime(
            elapsed, botdata[author]["total"])
        del botdata[author]["start"]
        botdata[author]["sessions"] += 1
    else:
        botdata[author]["total"] = addTimetoTime(
            elapsed, botdata[author]["total"])
        del botdata[author]["start"]
        botdata[author]["sessions"] += 1

    botdata[author]["status"] = "free"
    writeData()
    return (tt, elapsed)


"""
Input: Time format
Output: HH:MM:SS
"""


def extractTime(instr):
    instr = instr.strip()
    instr = instr.upper()
    hours = 0
    mins = 0
    secs = 0
    # 7.50
    x = re.match(r"^(\d{1,2}\.\d*) *(|PM|AM)$", instr)
    if (bool(x)):
        x = x.groups()
        infloat = int(x[0])
        hours = int(infloat) % 12
        infloat *= 60
        mins = int(infloat) % 60
        infloat *= 60
        secs = int(infloat) % 60
        if (instr.count("PM") > 0):
            hours += 12
    else:
        r = r"^(?:(\d{1,2})(?:|:)(\d{0,2})(?:|:) *(|AM|PM)|(\d{1,2}):(\d{1,2})(?:|:)(\d{0,2}) *(|AM|PM))$"
        x = re.match(r, instr)
        if (bool(x)):
            x = x.groups()
            if (x[0] != None):
                hours = int(x[0])
                hours = hours-12 if hours == 12 or hours == 24 else hours
                mins = int(x[1])
                if (x[2] == "PM" and hours < 12):
                    hours += 12
            else:
                hours = int(x[3]) % 12
                hours = hours-12 if hours == 12 or hours == 24 else hours
                mins = int(x[4])
                secs = int(x[5])
                if (x[6] == "PM" and hours < 12):
                    hours += 12
        else:
            # bad regex
            return "-1:-1:-1"
    hours %= 24
    mins %= 60
    secs %= 60
    hours = "0"+str(hours) if hours < 10 else hours
    mins = "0"+str(mins) if mins < 10 else mins
    secs = "0"+str(secs) if secs < 10 else secs

    return str(hours) + ":" + str(mins) + ":" + str(secs)


"""
IN: YYYY-MM-DD HH:mm:SS
OUT: YYYY-MM-DD HH:mm:SS
"""


def correctDate(author, theday="", boundary="none"):

    if (theday == ""):
        theday = getDateTime(botdata[author]["timezone"])
    if (theday.count("-") == 0):
        td1 = getDate(botdata[author]["timezone"])
        theday = td1 + " " + theday

    tmp = theday.split(" ")
    boundary = boundary.replace("up", "")
    time = tmp[1]
    date = tmp[0]

    if (boundary == "wake"):
        if (detWakeupBoundary(time)):
            theday = addDaytoDate(theday, 1)
    if (boundary == "sleep"):
        if (detSleepBoundary(time)):
            theday = addDaytoDate(theday, -1)
    if (boundary == "schoolstart"):
        if (detSchoolStartBoundary(time)):
            theday = addDaytoDate(theday, 1)
    if (boundary == "schoolend"):
        if (detSchoolEndBoundary(time)):
            theday = addDaytoDate(theday, -1)
    return theday


def logDates(author, theday, boundary="none"):
    date = correctDate(author, theday, boundary)
    date = date.split()[0]
    if (date not in botdata[author]):
        botdata[author][date] = {}
        writeData()


# calculate difference between end and start
# returns TIME
"""
IN: YYYY-MM-DD HH:mm:SS
OUT: HH:MM:SS
"""


def diffDatefromDate(start, end):
    start1 = start
    end1 = end
    start = datetime.fromisoformat(start)
    end = datetime.fromisoformat(end)
    diff = end-start
    if (not ("day" in str(diff))):
        diff = "0 days, "+str(diff)
    if ("-" in diff):
        return "-"+diffDatefromDate(end1, start1)
    diff = str(diff).split(", ")
    hms = diff[1]
    hms = hms.split(":")
    h = int(hms[0])
    m = int(hms[1])
    s = int(float(hms[2]))
    days = int(diff[0].split(" ")[0])
    h += 24*days
    h = "0"+str(h) if h < 10 else h
    m = "0"+str(m) if m < 10 else m
    s = "0"+str(s) if s < 10 else s
    return str(h)+":"+str(m)+":"+str(s)


"""
IN1: YYYY-MM-DD HH:mm:SS
IN2: #
OUT: YYYY-MM-DD HH:mm:SS
"""


def addDaytoDate(start, inc):
    start = datetime.fromisoformat(start) + timedelta(days=inc)
    return str(start)


def addHourtoDate(start, hrs):
    start = datetime.fromisoformat(start) + timedelta(hours=hrs)
    return str(start)


"""
IN - HH:MM:SS
OUT - HH:MM:SS
"""


def addTimetoTime(start, end):
    start = start.split(":")
    end = end.split(":")
    sh, sm, ss = (int(i) for i in start)
    eh, em, es = (int(i) for i in end)
    th = 0
    tm = 0
    ts = 0
    ts += ss+es
    tm += ts // 60
    ts %= 60
    tm += sm+em
    th += tm // 60
    tm %= 60
    th += eh+sh
    th = "0"+str(th) if th < 10 else th
    tm = "0"+str(tm) if tm < 10 else tm
    ts = "0"+str(ts) if ts < 10 else ts
    return str(th)+":"+str(tm)+":"+str(ts)


"""
Get time differnece
ex.
Between 23:00:00 and 05:00:00 is 06:00:00
Between 23:00:00 and 23:00:01 is 00:00:01
"""


def diffTimefromTime(start_time, end_time):
    def time_to_seconds(time_str):
        h, m, s = map(int, time_str.split(':'))
        return h * 3600 + m * 60 + s

    start_seconds = time_to_seconds(start_time)
    end_seconds = time_to_seconds(end_time)

    time_diff_seconds = end_seconds - start_seconds

    if time_diff_seconds < 0:
        time_diff_seconds += 24 * 3600

    hours = time_diff_seconds // 3600
    minutes = (time_diff_seconds % 3600) // 60
    seconds = time_diff_seconds % 60

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


"""
IN: HH:mm:SS
OUT: t/f

Determines whether to add +1 day beacuse we naturally stay up past 12:00 sometimes.

"""


def detSleepBoundary(intime):
    intime = [int(i) for i in intime.split(":")]
    dec = intime[0] + intime[1]/60 + intime[2]//3600
    if (dec > 0 and dec < float(botconf["nightboundary"])):
        return True
    return False


def detSchoolEndBoundary(intime):
    intime = [int(i) for i in intime.split(":")]
    dec = intime[0] + intime[1]/60 + intime[2]//3600
    if (dec > 0 and dec < float(botconf["schoolendboundary"])):
        return True
    return False


"""
IN: HH:mm:SS
OUT: t/f

the "opposite" of detSleepBoundary. Wakeup past XX:XX PM is considered "the next day" to account for detSleepBoundary's shift.
"""


def detWakeupBoundary(intime):
    intime = [int(i) for i in intime.split(":")]
    dec = intime[0] + intime[1]/60 + intime[2]//3600

    if (dec < 24 and dec > float(botconf["dayboundary"])):
        return True
    return False


def detSchoolStartBoundary(intime):
    intime = [int(i) for i in intime.split(":")]
    dec = intime[0] + intime[1]/60 + intime[2]//3600

    if (dec < 24 and dec > float(botconf["schoolstartboundary"])):
        return True
    return False


def checkTimeSpent(author, startbound, endbound, task=""):
    usrtimezone = botdata[author]["timezone"]
    startbound = addHourtoDate(startbound, -usrtimezone)
    endbound = addHourtoDate(endbound, -usrtimezone)

    logs = botdata[author]["sessionslist"]
    elapsed = [0, 0, 0]
    startbound = datetime.fromisoformat(startbound)
    endbound = datetime.fromisoformat(endbound)
    for i in logs:
        i = logs[i]
        if (task != ""):
            if (not len(i) == 3 or not i[2] == task):
                continue
        st = datetime.fromisoformat(i[0])
        et = datetime.fromisoformat(i[1])
        if (st < startbound):
            # case 2, 4, 5

            # case 5
            if (et < startbound):
                continue
            # case 4
            if (et > endbound):
                timediff = endbound - startbound
            else:
                timediff = et - startbound

        elif (st < endbound):
            # case 1, 3

            # case 1
            if (et < endbound):
                timediff = et - st
            else:
                timediff = endbound - st
        else:
            # case 1, 3, 6
            continue
        hrs = timediff.seconds//3600
        mins = (timediff.seconds//60) % 60
        secs = timediff.seconds % 60
        elapsed[2] += secs
        elapsed[1] += mins
        elapsed[0] += hrs

        elapsed[1] += elapsed[2]//60
        elapsed[2] = elapsed[2] % 60
        elapsed[0] += elapsed[1]//60
        elapsed[1] = elapsed[1] % 60
        # print(elapsed)
    elapsed[0] = "0"+str(elapsed[0]) if elapsed[0] < 10 else str(elapsed[0])
    elapsed[1] = "0"+str(elapsed[1]) if elapsed[1] < 10 else str(elapsed[1])
    elapsed[2] = "0"+str(elapsed[2]) if elapsed[2] < 10 else str(elapsed[2])

    return f"{elapsed[0]}:{elapsed[1]}:{elapsed[2]}"


def getProductivity(author, sdate, edate):
    st = sdate
    et = edate
    # waked = botdata[author][sdate.split()[0]]["wakeup"]
    # slept = botdata[author][edate.split()[0]]["sleep"]
    # if (detWakeupBoundary(waked)):
    #     st = addDaytoDate(st, -1).split()[0] + waked
    # if (detSleepBoundary(slept)):
    #     et = addDaytoDate(et, 1)+" "+

    print(st+"||"+et)
    worked = checkTimeSpent(author, st, et).split(":")
    total = diffDatefromDate(st, et).split(":")
    ws = int(worked[0])*3600 + int(worked[1])*60 + int(worked[2])
    ts = int(total[0])*3600 + int(total[1])*60 + int(total[2])
    return ws/ts
