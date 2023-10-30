from serial import Serial
from serial.threaded import ReaderThread, LineReader
from utils import get_serial_ports


class PortReader():
    port = None
    reader = None


class PrintLines(LineReader):
    def connection_made(self, transport):
        super(PrintLines, self).connection_made(transport)
        print("[connection_made] Connected, ready to receive data...")

    def handle_line(self, line):
        print("[handle_line] New line: {}".format(line))

    def connection_lost(self, exc):
        if self.transport.serial:
            print("[connection_lost] Port: [{}] closed".format(self.transport.serial.name))
            SystemPorts.remove(self.transport.serial.name)
        else:
            print("[connection_lost] Port closed")


class SystemPorts():

    _ports = {}

    _BAUD_RATE = 115200

    def get_ports_names():
        return SystemPorts._ports.keys()

    def init():
        for port_name in get_serial_ports():
            if not SystemPorts.get(port_name):
                SystemPorts.add(port_name)

            if not SystemPorts.port_is_open(port_name):
                SystemPorts.open_port(port_name)

    def add(port_name: str):
        if not port_name in SystemPorts._ports:
            SystemPorts._ports[port_name] = PortReader()

        SystemPorts._ports[port_name].port = Serial(port=port_name, baudrate=SystemPorts._BAUD_RATE)

        SystemPorts._ports[port_name].reader = ReaderThread(SystemPorts.get(port_name).port, PrintLines)
        SystemPorts._ports[port_name].reader.start()


    def get(port_name: str) -> PortReader:
        if port_name in SystemPorts._ports:
            return SystemPorts._ports[port_name]
        else:
            return None


    def remove(port_name):
        SystemPorts._ports.pop(port_name)


    def close_port(port_name: str):
        if SystemPorts.get(port_name).port:
            SystemPorts.get(port_name).port.close()


    def close_all_ports():
        for port_name in list(SystemPorts.get_ports_names()):
            SystemPorts.close_port(port_name)


    def port_is_open(port_name: str) -> bool:
        return SystemPorts.get(port_name).port.is_open


    def open_port(port_name: str):
        SystemPorts.get(port_name).port.open()


    def refresh():
        port_names = get_serial_ports()

        if len(port_names - SystemPorts.get_ports_names()) != 0:
            print("Ports changed: {}".format(port_names))
            SystemPorts.init()

