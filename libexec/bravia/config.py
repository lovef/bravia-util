#!/usr/bin/env python3

import json
from pathlib import Path

configDir = Path(__file__).parent / 'config'

ipFile = configDir / 'ip'

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

def read(fileName):
    configFile = configDir / fileName
    if configFile.exists():
        return configFile.read_text()

def write(data, fileName):
    configFile = configDir / fileName
    print('Write', data, 'to', configFile)
    configFile.parent.mkdir(parents=True, exist_ok=True)
    configFile.write_text(data)
    return configFile

if __name__ == '__main__':
    print(readIp())
