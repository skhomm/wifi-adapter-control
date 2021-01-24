import sys
import os
import subprocess


# we must be root to run this script - exit with msg if not
if not os.geteuid() == 0:
    print("\n#####################################################################################")
    print("You must be root to run this script (use 'sudo adapter_control.py') - exiting")
    print("#####################################################################################\n")
    sys.exit()

# Initialize variables in case we do not get any parameters passed to us
WLAN_PI_IFACE = 'wlan0'
CHANNEL_WIDTH = 'HT20'
CHANNEL_NUMBER = '36'
SLICE = '0'
FILTER = ' '
DEBUG = True

current_adapter = WLAN_PI_IFACE
current_channel = CHANNEL_NUMBER
current_width = CHANNEL_WIDTH


def change_mode(adapter, mode, channel, width):
    commands_list_managed = [
        ['Killing old tcpdump processes...', '/usr/bin/pkill -f tcpdump > /dev/null 2>&1'],
        ['Killing processes that may interfere with airmon-ng...', 'airmon-ng check kill > /dev/null 2>&1'],
        ['Bringing WLAN card up...', 'ifconfig {} up'.format(adapter)],
        ['Setting wireless adapter to managed mode', 'iw dev {} set type managed'.format(adapter)]
    ]

    commands_list_monitor = [
        ['Killing old tcpdump processes...', '/usr/bin/pkill -f tcpdump > /dev/null 2>&1'],
        ['Killing processes that may interfere with airmon-ng...', 'airmon-ng check kill > /dev/null 2>&1'],
        ['Bringing WLAN card up...', 'ifconfig {} up'.format(adapter)],
        ['Setting wireless adapter to monitor mode', 'iw {} set monitor none'.format(adapter)],
        ['Setting wireless adapter to channel {} (channel width {})'.format(channel, width), 'iw {} set channel {} {}'.format(adapter, channel, width)]
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
                    print("Error executing command: {} (Error msg: {})".format(command[1], ex))

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
                    print("Error executing command: {} (Error msg: {})".format(command[1], ex))
    else:
        print("Mode not selected")


def get_channel():
    global current_channel, current_width
    current_channel = input("\nType channel number and press Enter\n")
    current_width = input("\nType channel width and press Enter\n")


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
    subprocess.call('tcpdump -n -i {} -U -s {} -G 60 -w dump-%m%d-%H%M.pcap {}'.format(WLAN_PI_IFACE, SLICE, FILTER), shell=True)


def option_1():
    change_mode(WLAN_PI_IFACE, 'managed', current_channel, current_width)


def option_2():
    change_mode(WLAN_PI_IFACE, 'monitor', current_channel, current_width)


def option_3():
    get_channel()


menu()
