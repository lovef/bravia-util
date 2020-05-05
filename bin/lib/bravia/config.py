#!/usr/bin/env python3

import json
from pathlib import Path
import re
import time

configDir = Path(__file__).parent / 'config'

ipFile = configDir / 'ip'

propertyPattern = re.compile("(^|\n) *([^#\s]+) *= *([^#\s]+)")

def readIp():
    if ipFile.exists():
        return ipFile.read_text()

def writeIp(ip):
    print('Write', ip, 'to', ipFile)
    ipFile.parent.mkdir(parents=True, exist_ok=True)
    ipFile.write_text(ip)

def readAccessConfig(ip):
    data = read(f'{ip}.accessconfig.json')
    return json.loads(data) if data is not None else None

def writeAccessConfig(ip, accessConfig):
    data = json.dumps(accessConfig, indent=4)
    write(data, f'{ip}.accessconfig.json')

def readCookieCache(ip):
    data = read(f'{ip}.cookie.json')
    if data:
        parsed = json.loads(data)
        if parsed['bestBefore'] > time.time():
            return parsed['cookie']

def cacheCookie(ip, cookie):
    maxAge = int(re.search('Max-Age=(\d+)', cookie).group(1))
    data = json.dumps({'cookie': cookie, 'bestBefore': maxAge - 3 * 60 * 60 + time.time()}, indent=4)
    write(data, f'{ip}.cookie.json')

def readAliases():
    return readProperties('alias.properties')

def readCommands():
    return readProperties('commands.properties')

def readPreset():
    return read('preset')

def writeCommands(commands):
    properties = write(commands, 'commands.properties')

def readProperties(fileName):
    properties = read(fileName)
    if properties is None:
        return {}
    return {key: value for ignored, key, value in propertyPattern.findall(properties)}

def read(fileName):
    configFile = configDir / fileName
    if configFile.exists():
        return configFile.read_text()

def write(data, fileName):
    configFile = configDir / fileName
    configFile.parent.mkdir(parents=True, exist_ok=True)
    configFile.write_text(data)
    return configFile

if __name__ == '__main__':
    print(readIp())
