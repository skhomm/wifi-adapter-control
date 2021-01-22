import sys
import os
import subprocess

__author__ = 'Nigel Bowden'
__version__ = '0.05'
__email__ = 'wifinigel@gmail.com'
__status__ = 'beta'

# we must be root to run this script - exit with msg if not
if not os.geteuid() == 0:
    print("\n#####################################################################################")
    print("You must be root to run this script (use 'sudo wlanpishark.py') - exiting")
    print("#####################################################################################\n")
    sys.exit()

# Initialize variables in case we do not get any parameters passed to us
WLAN_PI_IFACE = 'wlan0'
CHANNEL_WIDTH = 'HT20'
CHANNEL_NUMBER = '36'
SLICE = '0'
FILTER = ' '
DEBUG = True

# These are the commands to get the WLANPi ready to stream the tcpdump data
commands_list_monitor = [
    ['Killing old tcpdump processes...', '/usr/bin/pkill -f tcpdump > /dev/null 2>&1'],
    ['Killing processes that may interfere with airmon-ng...', 'airmon-ng check kill > /dev/null 2>&1'],
    ['Bringing WLAN card up...', 'ifconfig {} up'.format(WLAN_PI_IFACE)],
    ['Setting wireless adapter to monitor mode', 'iw dev {} set managed'.format(WLAN_PI_IFACE)]
]

commands_list_managed = [
    ['Killing old tcpdump processes...', '/usr/bin/pkill -f tcpdump > /dev/null 2>&1'],
    ['Killing processes that may interfere with airmon-ng...', 'airmon-ng check kill > /dev/null 2>&1'],
    ['Bringing WLAN card up...', 'ifconfig {} up'.format(WLAN_PI_IFACE)],
    ['Setting wireless adapter to monitor mode', 'iw {} set monitor none'.format(WLAN_PI_IFACE)],
    ['Setting wireless adapter to channel {} (channel width {})'.format(CHANNEL_NUMBER, CHANNEL_WIDTH), 'iw {} set channel {} {}'.format(WLAN_PI_IFACE, CHANNEL_NUMBER, CHANNEL_WIDTH)],
]


def menu():
    print("Select task\n")
    print("[0] Change adapter mode")
    print("[1] Start packet capture")
    print("[2] Association Request analysis")
    print("[3] Start roaming test")


def option_0():
    # execute each command in turn
    for command in commands_list_monitor:

        if DEBUG:
            print(command[0])
            print("Command : " + str(command[1]))

        try:
            cmd_output = subprocess.call(command[1], shell=True)
            if DEBUG:
                print("Command output: " + str(cmd_output))
        except Exception as ex:
            if DEBUG:
                print("Error executing command: {} (Error msg: {})".format(command[1], ex))


def option_1():
    # execute each command in turn
    for command in commands_list_managed:

        if DEBUG:
            print(command[0])
            print("Command : " + str(command[1]))

        try:
            cmd_output = subprocess.call(command[1], shell=True)
            if DEBUG:
                print("Command output: " + str(cmd_output))
        except Exception as ex:
            if DEBUG:
                print("Error executing command: {} (Error msg: {})".format(command[1], ex))


menu()
task_chosen = input("\nType number and press Enter\n")

if task_chosen == "0":
    option_0()
elif task_chosen == "1":
    option_1()
