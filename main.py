import time
from utils import get_serial_ports
from serial import Serial
from serial.threaded import ReaderThread, LineReader
from threading import Thread
from typing import Dict

system_ports = {}


class PrintLines(LineReader):
    def connection_made(self, transport):
        super(PrintLines, self).connection_made(transport)
        print("[connection_made] Connected, ready to receive data...")

    def handle_line(self, line):
        print("[handle_line] New line: {}".format(line))

    def connection_lost(self, exc):
        print("[connection_lost] Port closed")
        # print_all(self)


def print_all(obj: object):
    for attr in dir(obj):
        print("{}: {}".format(attr, getattr(obj, attr)))


def re_open_port(port: Serial) -> bool:
    if not port.is_open:
        port.open()


def handle_ports():
    print("[handle_ports] Starting thread")

    while True:
        port_names = get_serial_ports()
        print("[handle_ports] Ports detected: {}".format(port_names))

        for port_name in port_names:
            if not port_name in system_ports:
                if not port_name in system_ports.keys():
                    system_ports[port_name] = {
                        "port": None,
                        "reader": None
                    }

                system_ports[port_name]["port"] = Serial(port=port_name, baudrate=115200)

            if not system_ports[port_name]["port"].is_open:
                system_ports[port_name]["port"].open()



            if system_ports[port_name]["reader"] is None:
                system_ports[port_name]["reader"] = ReaderThread(system_ports[port_name]["port"], PrintLines)
                system_ports[port_name]["reader"].start()

        time.sleep(1)


def handle_loop():
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print('Interrupted!')

if __name__ == '__main__':
    thread_ports = Thread(target=handle_ports)
    thread_loop = Thread(target=handle_loop)

    thread_ports.start()
    thread_loop.start()

    thread_ports.join()
    thread_loop.join()
