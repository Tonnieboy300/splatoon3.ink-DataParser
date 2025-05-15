import json
import time
import calendar
import colorama
import requests

from colorama import just_fix_windows_console

just_fix_windows_console()

battleTypeId = 2
validTypes = ["regularSchedules", "bankaraSchedules", "xSchedules"]
validMatchSettings = ["regularMatchSetting", "bankaraMatchSettings", "xMatchSetting"]
formattedSettings = [
    f"{colorama.Fore.GREEN}Regular Battle{colorama.Fore.RESET}",
    f"{colorama.Fore.YELLOW}Anarchy Battle{colorama.Fore.RESET}",
    f"{colorama.Fore.CYAN}X Battle{colorama.Fore.RESET}",
]

rawData = open("./schedules.json")
data = json.loads(rawData.read())


def getNode(schedule: str, timeIn: time.struct_time):
    nodes = data["data"][schedule]["nodes"]
    hour = int(time.strftime("%H", timeIn))
    if hour % 2 != 0:
        hour -= 1
    hour = f"{hour:02d}"
    for node in nodes:
        if node["startTime"] == time.strftime(f"%Y-%m-%dT{hour}:00:00Z", timeIn):
            return node


def getMatchSetting(setting: str, node: dict, *args):
    if setting == "bankaraMatchSettings":
        for maps in node[setting]:
            if len(args) == 0:
                raise Exception("Anarchy mode not defined.")
            if maps["bankaraMode"] == args[0]:
                return maps
    else:
        return node[setting]


def getMapNames(setting: dict):
    mapList = setting["vsStages"]
    mapAlpha = mapList[0]["name"]
    mapBeta = mapList[1]["name"]
    return (mapAlpha, mapBeta)


def getNodeEndTime(node: dict):
    endTime = time.strptime(node["endTime"], "%Y-%m-%dT%H:%M:%SZ")
    endTime = calendar.timegm(endTime)
    return endTime


def timeToFormattedLocal(changeTime: time.struct_time):
    changeTime = time.localtime(changeTime)
    changeTime = time.strftime("%H:%M", changeTime)
    return changeTime


if getNodeEndTime(
    data["data"]["regularSchedules"]["nodes"][
        len(data["data"]["regularSchedules"]["nodes"]) - 2
    ]
) < calendar.timegm(time.gmtime()):
    print("data seems old, updating now...")
    download = requests.get("https://splatoon3.ink/data/schedules.json")
    open("./schedules.json", "w").write(download.text)
    rawData = open("./schedules.json")
    data = json.loads(rawData.read())
    print("done!")

# only matters for bankara (anarchy)
validModes = ["CHALLENGE", "OPEN"]
formattedModes = ["Series", "Open"]
modeId = 0  # default

print(f"{colorama.Style.DIM}Current Time: {time.strftime('%H:%M', time.localtime())}")
while True:
    try:
        battleTypeId = int(
            input(
                f"{colorama.Style.NORMAL}Choose from the following:\n0 - {formattedSettings[0]}\n1 - {formattedSettings[1]} (default)\n2 - {formattedSettings[2]}\n"
            )
            or 1
        )
    except:
        print("Couldn't understand your input. Try again.")
        continue
    break

if battleTypeId == 1:
    while True:
        try:
            modeId = int(
                input(
                    f"Choose:\n0 - {formattedModes[0]} (default)\n1 - {formattedModes[1]}\n"
                )
                or 0
            )
        except:
            print("Couldn't understand your input. Try again.")
            continue
        break

battleType = validTypes[battleTypeId]
matchSetting = validMatchSettings[battleTypeId]

mode = validModes[modeId]

currentFormattedSetting = formattedSettings[battleTypeId]
seriesType = formattedModes[modeId]
currentFormattedSetting = (
    currentFormattedSetting
    if currentFormattedSetting != formattedSettings[1]
    else f"{currentFormattedSetting} {seriesType}"
)

currentNode = getNode(battleType, time.gmtime())
currentSetting = getMatchSetting(matchSetting, currentNode, mode)
currentMode = currentSetting["vsRule"]["name"]
currentMaps = getMapNames(currentSetting)

nodeEndTime = getNodeEndTime(currentNode)
changeTime = timeToFormattedLocal(nodeEndTime)

nextNode = getNode(battleType, time.gmtime(nodeEndTime))
nextSetting = getMatchSetting(matchSetting, nextNode, mode)
nextMode = nextSetting["vsRule"]["name"]
nextMaps = getMapNames(nextSetting)

nextNodeEndTime = getNodeEndTime(nextNode)
nextChangeTime = timeToFormattedLocal(nextNodeEndTime)

print(
    f"Currently on {currentFormattedSetting} until {changeTime}: {currentMode} on {currentMaps[0]} and {currentMaps[1]}."
)
print(
    f"{colorama.Style.DIM}Next from {changeTime} to {nextChangeTime}: {nextMode} on {nextMaps[0]} and {nextMaps[1]}{colorama.Style.RESET_ALL}"
)
print(f"{colorama.Style.DIM}Data from splatoon3.ink{colorama.Style.RESET_ALL}")
