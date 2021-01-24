"""
This module controls the wireless adapter mode and starts a capture if needed.

It provides an interactive shell to set all required parameters.
You may also find useful calling change_mode(adapter, mode, channel, width)
from other programms.
"""


import sys
import os
import subprocess


# we must be root to run this script - exit with msg if not
if not os.geteuid() == 0:
    print("\n#####################################################################################")
    print("You must be root to run this script (use 'sudo adapter_control.py') - exiting")
    print("#####################################################################################\n")
    sys.exit()

CHANNELS_2GHZ = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
CHANNELS_5GHZ = [
                36, 40, 44, 48,
                52, 56, 60, 64,
                100, 104, 108, 112, 116, 120, 124, 128, 132, 136, 140, 144,
                149, 153, 157, 161, 165
            ]
CHANNEL_WIDTHS = {1: 'HT20', 2: 'HT40-', 3: 'HT40+', 4: '80MHz'}

# Initialize variables in case we do not get any parameters passed to us
WLAN_PI_IFACE = 'wlan0'
CHANNEL_WIDTH = 'HT20'
CHANNEL_NUMBER = '36'
DEBUG = True
TCPDUMP_OPTIONS = '-G 60 -w dump-%m%d-%H%M.pcap'

current_adapter = WLAN_PI_IFACE
current_channel = CHANNEL_NUMBER
current_width = CHANNEL_WIDTH
current_tcpdump_options = TCPDUMP_OPTIONS


def change_mode(adapter, mode, channel, width):
    commands_list_managed = [
        ['Killing old tcpdump processes...', '/usr/bin/pkill -f tcpdump > /dev/null 2>&1'],
        ['Killing processes that may interfere with airmon-ng...', 'airmon-ng check kill > /dev/null 2>&1'],
        ['Bringing WLAN card up...', f'ifconfig {adapter} up'],
        ['Setting wireless adapter to managed mode', f'iw dev {adapter} set type managed']
    ]

    commands_list_monitor = [
        ['Killing old tcpdump processes...', '/usr/bin/pkill -f tcpdump > /dev/null 2>&1'],
        ['Killing processes that may interfere with airmon-ng...', 'airmon-ng check kill > /dev/null 2>&1'],
        ['Bringing WLAN card up...', f'ifconfig {adapter} up'],
        ['Setting wireless adapter to monitor mode', f'iw {adapter} set monitor none'],
        [f'Setting wireless adapter to channel {channel} (channel width {width})', 'iw {adapter} set channel {channel} {width}']
    ]

    if mode == 'managed':
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
                    print(f"Error executing command: {command[1]} (Error msg: {ex})")

    elif mode == 'monitor':
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
                    print(f"Error executing command: {command[1]} (Error msg: {ex})")
    else:
        print("Mode not selected")


def get_channel_number():
    global current_channel

    print(f"\nAvailable channels: \n2.4GHz: {CHANNELS_2GHZ} \n5GHz: {CHANNELS_5GHZ}")
    current_channel = input("\nType channel number and press Enter\n")

    while int(current_channel) not in (CHANNELS_2GHZ + CHANNELS_5GHZ):
        get_channel_number()


def get_channel_width():
    global current_width

    print(f"\nAvailable channelwidths: {CHANNEL_WIDTHS}")
    current_width_input = input("\nType channel width and press Enter\n")
    while int(current_width_input) not in CHANNEL_WIDTHS:
        get_channel_width()

    current_width = CHANNEL_WIDTHS[int(current_width_input)]


def start_tcpdump(adapter, options):
    subprocess.call(f'tcpdump -i {adapter} {options}', shell=True)


def menu():
    print(f"\nAdapter: {current_adapter}")
    print(f"Channel number: {current_channel}")
    print(f"Channel width: {current_width}")

    print("\nSelect task\n")
    print("[0] Start tcpdump")
    print("[1] Change adapter mode to MANAGED")
    print("[2] Change adapter mode to MONITOR")
    print("[3] Change channel number and width")

    task_chosen = input("\nType number and press Enter\n")

    if task_chosen == "0":
        option_0()
    elif task_chosen == "1":
        option_1()
    elif task_chosen == "2":
        option_2()
    elif task_chosen == "3":
        option_3()

    menu()


def option_0():
    start_tcpdump(current_adapter, current_tcpdump_options)


def option_1():
    change_mode(current_adapter, 'managed', current_channel, current_width)


def option_2():
    change_mode(current_adapter, 'monitor', current_channel, current_width)


def option_3():
    get_channel_number()
    get_channel_width()


if __name__ == '__main__':
    menu()
