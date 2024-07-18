#!/usr/bin/env python3

import sys
import requests
import ipaddress
import argparse
import concurrent.futures

def check_ip(ip, host,keyword,port):
    ip = ip.strip("\n")
    headers = {'Host':host}
    try:
        r = requests.get("http://"+str(ip)+":"+str(port),headers=headers, timeout=2)
        if keyword in r.text:
            print("Potential match with:","http://"+str(ip)+":"+str(port))
    except Exception as e:
        print("This address doesn't seem to work: ",e,file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description='Search for host in an ip range')
    parser.add_argument("--iprange", "-r", type=str, nargs="+", help="The ip range that we will search in", required=False)
    parser.add_argument("--file", "-f", type=str, nargs="+", help="File to store ips", required=False)
    parser.add_argument('--host', '-i', type=str, nargs="+", help="Host to search for", required=True)
    parser.add_argument('--port', '-p', type=int, nargs="+", help="Port to use", default=80)
    parser.add_argument('--keyword', '-k', type=str, nargs="+", help="Keyword to validate the page", required=True)
    parser.add_argument('--threads', '-t', type=int, nargs="+", help="Threads to power the scan", default=200)
    args = parser.parse_args()
    if args.file is not None:
        file_scan(args)
    elif args.iprange is not None:
        range_scan(args)
    else:
        print("You must specify a method to scan (Either file or iprange)")


def file_scan(args):
    file = str(args.file[0])
    host = str(args.host[0])
    keyword = str(args.keyword[0])
    port = args.port
    print("Range to scan:", range)
    print("Host to check:", host)
    print("Port:",port)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers = 400) as executor:
        future_to_url = {executor.submit(check_ip, ip, host, keyword, port): ip for ip in open(file).readlines()}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc),file=sys.stderr)

def range_scan(args):
    range = str(args.iprange[0])
    host = str(args.host[0])
    keyword = str(args.keyword[0])
    port = args.port
    print("Range to scan:", range)
    print("Host to check:", host)
    print("Port:",port)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers = 400) as executor:
        future_to_url = {executor.submit(check_ip, ip, host, keyword, port): ip for ip in ipaddress.IPv4Network(range, False)}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc),file=sys.stderr)
    
    

if __name__ == "__main__":
    main()
