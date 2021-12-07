#!/usr/bin/env python3

import sys
import requests
import ipaddress

def main():
    if len(sys.argv) == 4:
        range = sys.argv[1]
        host = sys.argv[2]
        port = sys.argv[3]
        print("Range to scan:", range)
        print("Host to check:", host)
        print("Port:",port)
        headers = {'Host':host}
        for ip in ipaddress.IPv4Network(range, False):
            print("Checking address:", ip)
            try:
                r = requests.get("http://"+str(ip)+":"+port,headers=headers, timeout=2)
                print(r.text)
            except:
                print("This address doesn't seem to work")
        
    else:
        print("Please launch the software using this command scheme: ./WebCheckHostRange.py 127.0.0.1/32 google.com 80")

if __name__ == "__main__":
    main()
