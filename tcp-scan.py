#!/bin/python3

import argparse
import socket
import binascii
import threading
import re

# semaphore will allow a function to have control of the screen, providing a lock to prevent other threads from proceeding
screen_lock = threading.Semaphore(value=1)

# define arguments
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--host', help='specify target host')
    parser.add_argument('-p', '--port', nargs='?', help='specify target port[s] separated by comma')
    options = parser.parse_args()
    tgtHost = options.host
    tgtPorts = str(options.port).split(',')
    if (tgtHost is None) | (tgtPorts[0] is None):
        parser.print_help
        exit(0)   
    portScan(tgtHost, tgtPorts)


def f_connect_scan(tgtHost, tgtPort):
    # create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # return error indicator instead of raising an exception for errors like connect()
    error = s.connect_ex((tgtHost, tgtPort))
    # if open the semaphore will grant us access to proceed and we will print to the screen.
    # if locked we will have to wait until the thread holding the semaphore releases the lock.
    screen_lock.acquire()
    if not error:
        print(f"[+] {tgtPort}/tcp open")
    else:
        print(f"[-] {tgtPort}/tcp closed")
    screen_lock.release()
    s.close()

def connScan(tgtHost, tgtPort):
    try:
        # create socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connect to ip address and port
        s.connect((tgtHost, tgtPort))
        # send string of data to the port and wait for response
        s.send(b"Isildur0x29A\r\n")
        res = s.recv(50)
        v = str(res)
        # remove html tags from the banner output
        clean = re.compile('<.*?>')
        v = re.sub(clean, '', v)
        # remove ' from the banner output
        clean = re.compile("[']")
        v = re.sub(clean, '', v)
        # remove the 'b' from the banner output
        clean = re.compile("[b]")
        v = re.sub(clean, '', v)
        screen_lock.acquire()
        print(f"[+]{tgtPort}/tcp open")
        print(f"[+] {v}")
    except:
        screen_lock.acquire()
        print(f"[-]{tgtPort}/tcp closed")
    finally:
        screen_lock.release()
        s.close()


def portScan(tgtHost, tgtPorts):
    try:
        # takes a hostname and returns an ipv4 address
        tgtIP = socket.gethostbyname(tgtHost)
    except:
        print(f"[-] Cannot resolve {tgtHost}: Unknown host")
        return
    try:
        # takes an ipv4 address and returns a triple containing the host name or alternative hostnames
        tgtName = socket.gethostbyaddr(tgtIP)
        print("\n[+} Scan Result for: " + tgtName[0])
    except:
        print("\n[+] Scan Result for: " + tgtIP)
    socket.setdefaulttimeout(1)
    
    for tgtPort in tgtPorts:
        t = threading.Thread(target=connScan, args=(tgtHost, int(tgtPort)))
        t.start()

if __name__ == '__main__':
    main()
