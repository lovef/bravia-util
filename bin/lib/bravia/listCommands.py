import sys
import shutil
import math

from . import server
from . import config

def main():
    commands = getCommands()
    table(commands)


def getCommands():
    commands = config.readCommands()
    if not commands:
        saveCommands()
        commands = config.readCommands()
    return commands

def table(commands):
    width = shutil.get_terminal_size((80, 20)).columns
    commandNames = list(commands.keys())
    maxColumnWidth = len(max(commandNames, key=len)) + 2
    columns = int(width / maxColumnWidth)
    columns = columns if columns >= 1 else 1
    lines = math.ceil(len(commands) / columns)
    for l in range(lines):
        line = ""
        for c in range(columns):
            index = l + c * lines
            if index >= len(commandNames):
                break
            value = commandNames[index]
            line = f"{line}{value:{maxColumnWidth}}"
        print(line.rstrip())

def saveCommands():
    commands = requestCommands()
    aliases = config.readAliases()

    propertiesText = ""
    for alias in aliases:
        try:
            command = commands[aliases[alias]]
            propertiesText = propertiesText + f"{alias:30} = {command}\n"
        except:
            propertiesText = propertiesText + f"# Could not resolve {alias} = {aliases[alias]}\n"

    if len(propertiesText) > 0:
        propertiesText = f"# Aliases:\n{propertiesText}\n"

    propertiesText = f"{propertiesText}# Commands:\n"

    for command in commands:
        propertiesText = propertiesText + f"{command:30} = {commands[command]}\n"

    config.writeCommands(propertiesText)

def requestCommands():
    server.setup(False)
    response = server.get('sony/system', {
        "id": 20,
        "method": "getRemoteControllerInfo",
        "version": "1.0",
        "params": []
    })
    for result in response["result"]:
        if isinstance(result, list):
            return { decapitalize(param['name']): param['value'] for param in result }

def decapitalize(string):
    return string[0].lower() + string[1:]
