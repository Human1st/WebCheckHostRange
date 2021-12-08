#!/usr/bin/env python3

import sys
import requests
import ipaddress
import argparse

def main():
    parser = argparse.ArgumentParser(description='Search for host in an ip range')
    parser.add_argument("--iprange", "-r", type=str, nargs="+", help="The ip range that we will search in", required=True)
    parser.add_argument('--host', '-i', type=str, nargs="+", help="Host to search for", required=True)
    parser.add_argument('--port', '-p', type=int, nargs="+", help="Port to use", default=80)
    args = parser.parse_args()
    range = str(args.iprange[0])
    host = str(args.host[0])
    port = args.port
    print("Range to scan:", range)
    print("Host to check:", host)
    print("Port:",port)
    headers = {'Host':host}
    for ip in ipaddress.IPv4Network(range, False):
        print("Checking address:", ip)
        try:
            r = requests.get("http://"+str(ip)+":"+str(port),headers=headers, timeout=2)
            print(r.text)
        except:
            print("This address doesn't seem to work")

if __name__ == "__main__":
    main()
