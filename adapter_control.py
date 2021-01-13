import sys
import os
import getopt
import subprocess

__author__ = 'Nigel Bowden'
__version__ = '0.05'
__email__ = 'wifinigel@gmail.com'
__status__ = 'beta'

# we must be root to run this script - exit with msg if not
if not os.geteuid()==0:
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
DEBUG = False


# These are the commands to get the WLANPi ready to stream the tcpdump data
commands_list = [
    [ 'Killing old tcpdump processes...', '/usr/bin/pkill -f tcpdump > /dev/null 2>&1'],
    [ 'Killing processes that may interfere with airmon-ng...', 'airmon-ng check kill > /dev/null 2>&1' ],
    [ 'Bringing WLAN card up...', 'ifconfig {} up'.format(WLAN_PI_IFACE) ],
    [ 'Setting wireless adapter to monitor mode', 'iw {} set monitor none'.format(WLAN_PI_IFACE) ],
    [ 'Setting wireless adapter to channel {} (channel width {})'.format(CHANNEL_NUMBER, CHANNEL_WIDTH), 'iw {} set channel {} {}'.format(WLAN_PI_IFACE, CHANNEL_NUMBER, CHANNEL_WIDTH) ],
    
]

# execute each command in turn
for command in commands_list:

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