#!/usr/bin/env python3

import config
import setup
import sys
import re
import time
from datetime import datetime
import urllib.request
import json
import secrets
import uuid
import platform
import base64
import server
from common import printerr

def main(script):
    ip = setup.main(script)
    cookie = getCookie(ip, script)
    return cookie

def getCookie(ip, script):
    access = getAccessConfig(ip, script)
    try:
        cookie = access["cookie"]
        bestBefore = datetime.fromisoformat(cookie["bestBefore"])
        if bestBefore > datetime.now():
            printerr("Use cached cookie for", access["name"])
            return cookie["data"]
    except:
        pass
    cookie = requestCookie(ip, access, script)
    maxAge = int(re.search('Max-Age=(\d+)', cookie).group(1))
    bestBefore = maxAge - 3 * 60 * 60 + time.time()

    access["cookie"] = {
        "data": cookie,
        "bestBefore": datetime.fromtimestamp(bestBefore).isoformat(sep=' ')
    }
    config.writeAccessConfig(ip, access)
    return cookie

def requestCookie(ip, access, script):
    # https://pro-bravia.sony.net/develop/integrate/rest-api/spec/index.html
    server.setup(ip)
    data = json.dumps(access["identity"]).encode("utf-8")
    print(data)

    url = f"http://{ip}/sony/accessControl"

    try:
        return server.requestCookie(url, data)
    except urllib.error.HTTPError as e:
        printerr(e.code, e.reason)
        if e.code == 401:
            auth = getAuthHeader(script)
            return server.requestCookie(url, data, auth)
        raise e

def getAuthHeader(script):
    if script:
        raise NameError('Cannot setup acces in script mode')
    code = input("Code from the TV: ")
    codeBase64 = base64.b64encode(f":{code}".encode('UTF-8')).decode()
    return f"Basic {codeBase64}"

def getAccessConfig(ip, script):
    access = config.readAccessConfig(ip)
    if access is None:
        if script:
            raise NameError('Cannot setup acces in script mode')
        access = setupAccess(ip)
    return access

def setupAccess(ip):
    uuidString = str(uuid.UUID(bytes=secrets.token_bytes(16)))
    host = platform.node()
    date = datetime.now().isoformat(sep=' ', timespec='minutes')
    name = f"{host} {date}"
    access = {
        "name": name,
        "identity": {
            "method": "actRegister",
            "id": 8,
            "version": "1.0",
            "params": [
                {
                    "clientid": f"{ip}:{uuidString}",
                    "nickname": name,
                    "level": "private"
                },
                [{"value": "yes", "function": "WOL"}]
            ]
        }
    }
    config.writeAccessConfig(ip, access)
    return access

if __name__ == '__main__':
    cookie = main(len(sys.argv) > 1 and sys.argv[1] == 'true')
    print(cookie)
