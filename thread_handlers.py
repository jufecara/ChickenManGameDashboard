import time
from threading import Event

from system import SystemPorts
from commands import get_all_points, reset_all

def handle_ports(event: Event):
    print("[handle_ports] Starting thread")
    while True:
        # If this event is set we must terminate the thread
        if event.is_set():
            break

        SystemPorts.refresh()

        time.sleep(0.5)


def handle_get_points(event: Event):
    print("[handle_get_points] Starting thread")
    while True:
        # If this event is set we must terminate the thread
        if event.is_set():
            break

        get_all_points()

        time.sleep(5)


def handle_input(event: Event):
    print("[handle_input] Starting thread")
    while True:
        if event.is_set():
            break;

        command = input()
        if command and len(command) > 1:
            print("[handle_input] Command received [{}]".format(command))
            if command == "reset":
                print("[handle_input] reseting devices")
                reset_all()

            if command == "points":
                print("[handle_input] requesting points")
                get_all_points()

            command = None
