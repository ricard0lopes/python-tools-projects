#!/usr/bin/env python3

'''
Python nmap scanner that goes through a list of the most common ports and check if their open + their service name.
Usage: python3 nmap-scan.py -H <ipaddress>
'''

import argparse
import nmap
import socket

# get arguments
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--host', dest='tgt_host', help='specify target host')
    options = parser.parse_args()
    tgt_host = options.tgt_host
    if tgt_host is None:
        parser.print_usage()
        exit(0)
    nmap_scan(tgt_host, tgt_port='')

# scan all common ports
def nmap_scan(tgt_host, tgt_port):
    common_ports = [21, 22, 23, 25, 53, 79, 80, 88, 110, 111, 135, 137, 139, 145, 161, 162, 389, 443, 
    587, 631, 636, 1433, 1521, 1723, 2049, 2100, 3306, 3389, 5900, 5985, 6379, 8080, 11211]
    for port in common_ports:
        try:
            tgt_port = port
            nm_scan = nmap.PortScanner()
            nm_scan.scan(tgt_host, str(tgt_port))
            # get state (open/close)
            state = nm_scan[tgt_host]['tcp'][int(tgt_port)]['state']
            # get service name
            service = socket.getservbyport(tgt_port)
            print(f"[*] {tgt_host} tcp/ {tgt_port} {state} {service}")
        # handle error when no service is found on that port
        except:
            continue

if __name__ == '__main__':
    main()
