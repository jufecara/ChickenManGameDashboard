import time
from threading import Event
from re import findall

from system_ports import SystemPorts
from commands import get_all_points, reset_all
from parse_data import get_id


def handle_ports(event: Event):
    print("[handle_ports] Starting thread")
    while True:
        # If this event is set we must terminate the thread
        if event.is_set():
            print("[handle_ports] Closing thread")
            break

        SystemPorts.refresh()

        time.sleep(0.5)


def handle_get_points(event: Event):
    print("[handle_get_points] Starting thread")
    while True:
        # If this event is set we must terminate the thread
        if event.is_set():
            print("[handle_get_points] Closing thread")
            break

        get_all_points()

        time.sleep(5)


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

            if command.startswith("show"):
                results = findall(r"^show\s(\d+)$", command)
                id = results[0]
                if id:
                    print(
                        "[handle_input] details of [{}]: {}".format(
                            id, SystemPorts._hosts[id].__dict__
                        )
                    )

            command = None
