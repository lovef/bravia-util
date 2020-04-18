#!/usr/bin/env python3

import config
import setup
import sys
import urllib.request
import http.client
import json
import secrets
import uuid
import platform
import datetime
import base64

def main(script):
    ip = setup.main(script)
    cookie = getCookie(ip, script)
    return cookie

def getCookie(ip, script):
    # https://pro-bravia.sony.net/develop/integrate/rest-api/spec/index.html
    access = getAccessConfig(ip, script)
    data = json.dumps(access).encode("utf-8")
    print(data)

    url = f"http://{ip}/sony/accessControl"

    try:
        return requestCookie(url, data)
    except urllib.error.HTTPError as e:
        print(e.code, e.reason)
        if e.code == 401:
            auth = getAuthHeader(script)
            return requestCookie(url, data, auth)
        raise e

def requestCookie(url, data, auth = None):
    headers = { "Authorization": auth } if auth is not None else {}
    req = urllib.request.Request(url, data, headers)
    response = urllib.request.urlopen(req)
    return response.info()['Set-Cookie']

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
    date = datetime.datetime.now().date().isoformat()
    accessConfig = {
        "method": "actRegister",
        "id": 8,
        "version": "1.0",
        "params": [
            {
                "clientid": f"{ip}:{uuidString}",
                "nickname": f"{host}-{date}",
                "level": "private"
            },
            [{"value": "yes", "function": "WOL"}]
        ]
    }
    config.writeAccessConfig(ip, accessConfig)
    return accessConfig

if __name__ == '__main__':
    cookie = main(len(sys.argv) > 1 and sys.argv[1] == 'true')
    print(cookie)
