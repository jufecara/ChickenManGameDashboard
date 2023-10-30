import time
from utils import get_serial_ports
from serial import Serial
from serial.threaded import ReaderThread, LineReader
from threading import Thread, Event


system_ports = {}


class PrintLines(LineReader):
    def connection_made(self, transport):
        super(PrintLines, self).connection_made(transport)
        print("[connection_made] Connected, ready to receive data...")

    def handle_line(self, line):
        print("[handle_line] New line: {}".format(line))

    def connection_lost(self, exc):
        if self.transport.serial:
            print("[connection_lost] Port: [{}] closed".format(self.transport.serial.name))
            system_ports[self.transport.serial.name] = None
        else:
            print("[connection_lost] Port closed")


def handle_ports(event: Event):
    print("[handle_ports] Starting thread")

    while True:
        port_names = get_serial_ports()

        if len(port_names - system_ports.keys()) != 0:
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

        if event.is_set():
            break

        time.sleep(0.5)


if __name__ == '__main__':
    try:
        event = Event()
        thread_ports = Thread(target=handle_ports, args=(event,))
        thread_ports.start()

        while True:
            pass

        event.set()
        thread_ports.join()

    except (KeyboardInterrupt, SystemExit):
        print('Interrupted!')
    finally:
        event.set()

        print("Program terminated")
