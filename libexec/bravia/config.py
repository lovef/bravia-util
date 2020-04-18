#!/usr/bin/env python3

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

if __name__ == '__main__':
    print(readIp())
