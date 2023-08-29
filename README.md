# PunchCard

A timecard-based productivity logging discord bot.

### Motivation

Most study/productivity discord bots are checklist-based, enabling each user to have a to-do list to check off daily tasks.

However, tasks are often repeated as a schedule a majority of the time instead of a simple to-do list. My experience of these discord bots involved re-inputting the same daily tasks onto the bot only to be checked off by the end of the day.

This bot, on the other hand, takes an alternative approach, by allowing the user to clock in and clock out of tasks daily instead of checking them off. It allows the user to log and keep track of the amount of time spent on particular recurring tasks.

## Setup

**1)** Get a bot token from the [Discord Developer Portal](https://discord.com/developers/applications)

**2)** First, clone this git repo

```
git clone https://github.com/vninja007/PunchCard.git
```

**3)** Then make a file called `./config.yml`, and put in the following values:

```
timezone: string+float, from UTC-12.0 to UTC+14.0 of the itme zone of the bot hosting
version: any string, does not matter.
nightboundary: float, determines the maximum sleeping time (set this number near 0-11 = 12AM-11AM)
dayboundary: float, determines the minimum wakeup time (set this number near 0-2 = 12AM-2AM)
schoolstartboundary: float, determines the maximum school starting time (set this near 14-20 = 2PM-8PM)
schoolendboundary: float, determines the minimum school ending time (set this near 0-3 = 12AM-3AM)
```

My `./config.yml` looks something like this:

```
#timezone where bot is hosted
timezone: "UTC-4"
version: "0.1"
nightboundary: 11.5
dayboundary: 23.5
schoolstartboundary: 18
schoolendboundary: 3
```

**4)** Make a `./punchcard/key.key` file, just with your discord bot key

**5)** Install requirements with `pip install -r ./requirements.txt`

## Launch

```
cd punchcard
python main.py
```

Terminate program with CTRL+C
e
