#!/usr/bin/env python3

import sys
import requests
import ipaddress
import argparse
import concurrent.futures
import random

def check_ip(ip, host,keyword,port):
    headers = {'Host':host}
    try:
        if port == 443:
            url = "https://"+str(ip)
        else:
            url = "http://"+str(ip)+":"+str(port)
        response = requests.get(url,headers=headers, timeout=2)
        if keyword in response.text:
            print("Keyword match with:","http://"+str(ip)+":"+str(port),host)
        else:
            headers = {'Host':"nohost.com"}
            response2 = requests.get(url,headers=headers, timeout=2)
            if len(response.text) != len(response2.text):
                print("Differencial match with:","http://"+str(ip)+":"+str(port),host)
    except Exception as e:
        print("This address doesn't seem to work: ",e,file=sys.stderr)
def scan(ips, host, keyword, port):
    random.shuffle(ips) # Shuffling IPs to avoid AS scan detection
    with concurrent.futures.ThreadPoolExecutor(max_workers = 400) as executor:
        future_to_url = {executor.submit(check_ip, ip, host, keyword, port): ip for ip in ips}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc),file=sys.stderr)
def launchIpScan(host, keyword, port, args):
    if args.file is not None:
        file = str(args.file[0])
        print("File to scan:", file)
        print("Host to check:", host)
        print("Port:",port)
        ips = []
        for ip in open(file).readlines():
            ips.append(ip.strip("\n"))
        scan(ips, host, keyword, port)
    elif args.iprange is not None:
        range = str(args.iprange[0])
        print("Range to scan:", range)
        print("Host to check:", host)
        print("Port:",port)
        scan(ipaddress.IPv4Network(range, False), host, keyword, port)
    else:
        print("You must specify a method to scan (Either file or iprange)")

def main():
    parser = argparse.ArgumentParser(description='Search for host in an ip range')
    parser.add_argument("--iprange", "-r", type=str, nargs="+", help="The ip range that we will search in", required=False)
    parser.add_argument("--file", "-f", type=str, nargs="+", help="File to store ips", required=False)
    parser.add_argument('--host', '-i', type=str, nargs="+", help="Host to search for", required=False)
    parser.add_argument('--hosts', '-s', type=str, nargs="+", help="Hosts file to search for", required=False)
    parser.add_argument('--port', '-p', type=int, nargs="+", help="Port to use", default=80)
    parser.add_argument('--keyword', '-k', type=str, nargs="+", help="Keyword to validate the page", required=True)
    parser.add_argument('--threads', '-t', type=int, nargs="+", help="Threads to power the scan", default=200)
    args = parser.parse_args()

    keyword = str(args.keyword[0])
    port = args.port
    if args.hosts is not None:
        for host in open(str(args.hosts[0])).readlines():
            host = host.strip("\n")
            launchIpScan(host, keyword, port, args)
    elif args.host is not None:
        launchIpScan(str(args.host[0]), keyword, port, args)
    else:
        print("You must specify host with a file or a host")
    

if __name__ == "__main__":
    main()
