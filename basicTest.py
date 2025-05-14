import json
import time
import calendar

validTypes = ["regularSchedules", "bankaraSchedules", "xSchedules"]
battleType = validTypes[1]
# only matters for bankara (anarchy)
validModes = ["CHALLENGE", "OPEN"]
mode = validModes[0]

rawData = open("./schedules.json")
data = json.loads(rawData.read())
desiredSchedule = data["data"][battleType]["nodes"]

# get current hour, and convert to previous even GMT hour
currentTime = int(time.strftime("%H", time.gmtime()))
if (currentTime % 2) != 0:
    currentTime -= 1

# get the current schedule for the desired mode
currentSchedule = None

for node in desiredSchedule:
    startTimeData = list(node["startTime"])
    startTime = int(startTimeData[11] + startTimeData[12])
    if startTime == currentTime:
        currentSchedule = node
        break

# for bankara, get the correct series type
mapSet = None

if battleType == "bankaraSchedules":
    for node in currentSchedule["bankaraMatchSettings"]:
        if node["bankaraMode"] == mode:
            mapSet = node
            break
else:
    mapSet = (
        currentSchedule["regularMatchSetting"]
        if (battleType == "regularSchedules")
        else currentSchedule["xMatchSetting"]
    )

mapAlphaName = mapSet["vsStages"][0]["name"]
mapBetaName = mapSet["vsStages"][1]["name"]
if battleType == "bankaraSchedules":
    seriesType = "Series" if mode == "CHALLENGE" else "Open"
else:
    seriesType = "X Battle" if battleType == "xSchedules" else "Regular Battle"
gameMode = mapSet["vsRule"]["name"]
endTime = time.strptime(currentSchedule["endTime"], "%Y-%m-%dT%H:%M:%SZ")
endTime = calendar.timegm(endTime)
endTime = time.localtime(endTime)
endTime = time.strftime("%H:%M", endTime)

print(
    f"Currently on {seriesType}: {gameMode} on {mapAlphaName} and {mapBetaName} until {endTime}"
)
# print(type(mapSet))
