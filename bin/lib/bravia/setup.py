import sys

from . import config
from . import selectIp
from .common import printerr

def main():
    ip = config.readIp()
    if ip == None:
        if config.getScript():
            raise NameError('Cannot select IP in script mode')
        ip = selectIp.main()
    return ip
