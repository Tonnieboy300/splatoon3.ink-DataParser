import json
import time
import calendar
import colorama
import requests

from colorama import just_fix_windows_console

just_fix_windows_console()

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

print(
    f"{colorama.Style.DIM}Current Time: {time.strftime('%H:%M', time.localtime())}{colorama.Style.NORMAL}"
)


regularBattleNode = getNode(validTypes[0], time.gmtime())
regularBattle = getMatchSetting(validMatchSettings[0], regularBattleNode)
regularBattleMaps = getMapNames(regularBattle)
nodeEndTime = getNodeEndTime(regularBattleNode)
nextRegularNode = getNode(validTypes[0], time.gmtime(nodeEndTime))
nextRegular = getMatchSetting(validMatchSettings[0], nextRegularNode)
nextRegularMaps = getMapNames(nextRegular)
changeTime = timeToFormattedLocal(nodeEndTime)
nextChangeTime = timeToFormattedLocal(getNodeEndTime(nextRegularNode))

print(f"Schedule until {changeTime}")
print(
    f"{colorama.Style.DIM}Schedule from {changeTime} until {nextChangeTime}{colorama.Style.NORMAL}\n"
)

print(
    f"{formattedSettings[0]}: {regularBattle['vsRule']['name']} on {regularBattleMaps[0]} and {regularBattleMaps[1]}"
)
print(
    f"{colorama.Style.DIM}{nextRegular['vsRule']['name']} on {nextRegularMaps[0]} and {nextRegularMaps[1]}{colorama.Style.NORMAL}\n"
)

anarchyBattleNode = getNode(validTypes[1], time.gmtime())
anarchyBattleS = getMatchSetting(
    validMatchSettings[1], anarchyBattleNode, validModes[0]
)
anarchyMapS = getMapNames(anarchyBattleS)
anarchyBattleO = getMatchSetting(
    validMatchSettings[1], anarchyBattleNode, validModes[1]
)
anarchyMapO = getMapNames(anarchyBattleO)


nextAnarchyNode = getNode(validTypes[1], time.gmtime(nodeEndTime))
nextAnarchyBattleS = getMatchSetting(
    validMatchSettings[1], nextAnarchyNode, validModes[0]
)
nextAnarchyMapS = getMapNames(nextAnarchyBattleS)
nextAnarchyBattleO = getMatchSetting(
    validMatchSettings[1], nextAnarchyNode, validModes[1]
)
nextAnarchyMapO = getMapNames(nextAnarchyBattleO)

print(
    f"{formattedSettings[1]} {formattedModes[0]}: {anarchyBattleS['vsRule']['name']} on {anarchyMapS[0]} and {anarchyMapS[1]}"
)
print(
    f"{colorama.Style.DIM}{nextAnarchyBattleS['vsRule']['name']} on {nextAnarchyMapS[0]} and {nextAnarchyMapS[1]}{colorama.Style.NORMAL}\n"
)

print(
    f"{formattedSettings[1]} {formattedModes[1]}: {anarchyBattleO['vsRule']['name']} on {anarchyMapO[0]} and {anarchyMapO[1]}"
)
print(
    f"{colorama.Style.DIM}{nextAnarchyBattleO['vsRule']['name']} on {nextAnarchyMapO[0]} and {nextAnarchyMapO[1]}{colorama.Style.NORMAL}\n"
)

xBattleNode = getNode(validTypes[2], time.gmtime())
xBattle = getMatchSetting(validMatchSettings[2], xBattleNode)
xBattleMaps = getMapNames(xBattle)

nextXBattleNode = getNode(validTypes[2], time.gmtime(nodeEndTime))
nextXBattle = getMatchSetting(validMatchSettings[2], nextXBattleNode)
nextXBattleMaps = getMapNames(nextXBattle)

print(
    f"{formattedSettings[2]}: {xBattle['vsRule']['name']} on {xBattleMaps[0]} and {xBattleMaps[1]}"
)
print(
    f"{colorama.Style.DIM}{nextXBattle['vsRule']['name']} on {nextXBattleMaps[0]} and {nextXBattleMaps[1]}{colorama.Style.NORMAL}\n"
)

print(f"{colorama.Style.DIM}Data from splatoon3.ink{colorama.Style.NORMAL}")
