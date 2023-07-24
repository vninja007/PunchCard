import re
from basics import getDate
from startup import botdata
from basics import writeData


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
            print(x)
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


def logDates(author):
    if (getDate() not in botdata[author]):
        botdata[author][getDate()] = {}
        writeData()


# calculate differnece between end and start
def timeDiff(start, end):
    pass
