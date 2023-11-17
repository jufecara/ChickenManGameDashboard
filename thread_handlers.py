import time
import os
from threading import Event

from system_ports import SystemPorts
from commands import get_all_points, reset_all

SLEEP_TIME_GET_POINTS = float(os.environ.get("SLEEP_TIME_GET_POINTS", 10))
SLEEP_TIME_SERIAL_PORTS = float(os.environ.get("SLEEP_TIME_SERIAL_PORTS", 0.5))


def handle_ports(event: Event):
    print("[handle_ports] Starting thread")
    while True:
        # If this event is set we must terminate the thread
        if event.is_set():
            print("[handle_ports] Closing thread")
            break

        SystemPorts.refresh()

        time.sleep(SLEEP_TIME_SERIAL_PORTS)


def handle_get_points(event: Event):
    print("[handle_get_points] Starting thread")
    while True:
        # If this event is set we must terminate the thread
        if event.is_set():
            print("[handle_get_points] Closing thread")
            break

        get_all_points()

        time.sleep(SLEEP_TIME_GET_POINTS)


def handle_input(event: Event):
    print("[handle_input] Starting thread")
    while True:
        if event.is_set():
            print("[handle_input] Closing thread")
            break

        command = input("Enter command > \n")
        if command and len(command) > 1:
            print("[handle_input] Command received [{}]".format(command))
            if command == "reset":
                print("[handle_input] reseting devices")
                reset_all()

            if command == "points":
                print("[handle_input] requesting points")
                get_all_points()

            command = None
