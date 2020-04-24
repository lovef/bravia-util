#!/usr/bin/env python3

import urllib.request
import json
import setup as setup_script
import access
import time
from common import printerr

ip = None
cookie = None

def setup(script):
    global ip
    ip = setup_script.main(script)

def setupAccess(script):
    setup(script)
    global cookie
    cookie = access.main(script)

def get(path, jsonData):
    data = json.dumps(jsonData).encode("utf-8")
    req = urllib.request.Request(f"http://{ip}/{path}", data)
    response = sendRequest(req, "GET " + path)
    return json.loads(response.read())

def command(command, code):
    data = f"""<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
        <s:Body>
            <u:X_SendIRCC xmlns:u="urn:schemas-sony-com:service:IRCC:1">
                <IRCCCode>{code}</IRCCCode>
            </u:X_SendIRCC>
        </s:Body>
    </s:Envelope>""".encode("ascii")
    headers = {
        "Cookie": cookie,
        "SOAPACTION": '"urn:schemas-sony-com:service:IRCC:1#X_SendIRCC"'
    }
    req = urllib.request.Request(f"http://{ip}/sony/ircc", data, headers, method="POST")
    response = sendRequest(req, f"IRCC {command} {code}")

def requestCookie(url, data, auth = None):
    headers = { "Authorization": auth } if auth is not None else {}
    req = urllib.request.Request(url, data, headers)
    response = sendRequest(req, "Request cookie")
    return response.info()['Set-Cookie']

def sendRequest(request, log):
    statusString = "failed"
    try:
        printerr(log, end =" .. ")
        start = time.time()
        response = urllib.request.urlopen(request)
        statusString = f"{response.getcode()}"
        return response
    finally:
        end = time.time()
        printerr(statusString, f"in {end - start:.3f}", prefix = None)
