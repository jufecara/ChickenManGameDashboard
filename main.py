import time
from utils import get_serial_ports
from commands import get_all_points
from threading import Thread, Event
from system import SystemPorts


def handle_ports(event: Event):
    print("[handle_ports] Starting thread")
    while True:
        # If this event is set we must terminate the thread
        if event.is_set():
            break

        SystemPorts.refresh()

        time.sleep(0.5)


def get_points(event: Event):
    print("[get_points]")
    while True:
        # If this event is set we must terminate the thread
        if event.is_set():
            break

        get_all_points()

        time.sleep(5)


if __name__ == '__main__':
    try:
        ports_event = Event()
        points_event = Event()

        # get the system serial ports
        SystemPorts.init()

        thread_ports = Thread(target=handle_ports, args=(ports_event,))
        thread_points = Thread(target=get_points, args=(points_event,))
        thread_ports.start()
        thread_points.start()

        while True:
            pass

        ports_event.set()
        points_event.set()

        thread_ports.join()
        thread_points.join()

    except (KeyboardInterrupt, SystemExit):
        print('Interrupted!')
    finally:
        ports_event.set()
        points_event.set()

        SystemPorts.close_all_ports()

        print("Script terminated")
