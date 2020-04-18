#!/usr/bin/env python3

import config
import selectIp
import sys

def main(script):
    ip = config.readIp()
    if ip == None:
        if script:
            raise NameError('Cannot select IP in script mode')
        ip = selectIp.main()
    return ip

if __name__ == '__main__':
    ip = main(len(sys.argv) > 1 and sys.argv[1] == 'true')
    print(ip)
