from serial import Serial
from serial.threaded import ReaderThread, LineReader

import ws_service
from utils import get_serial_ports
from parse_data import get_points
from game import Host


class PortReader:
    port = None
    reader = None


def line_handler(line: str, hosts):
    result = get_points(line)
    if len(result) > 0:
        ws_service.server.send_message_to_all(line)

        id = result[0][0]
        red = result[0][1]
        green = result[0][2]
        blue = result[0][3]

        if not id in hosts:
            hosts[id] = Host()

            hosts[id].set_points({"red": red, "green": green, "blue": blue})


class PrintLines(LineReader):
    def connection_made(self, transport):
        super(PrintLines, self).connection_made(transport)
        print("[connection_made] Connected, ready to receive data...")

    def handle_line(self, line):
        try:
            print("[handle_line] New line: {}".format(line))

            line_handler(line, SystemPorts._hosts)

        except Exception as exc:
            print("Exception: {}".format(exc))

    def connection_lost(self, exc):
        if self.transport.serial:
            print(
                "[connection_lost] Port: [{}] closed".format(self.transport.serial.name)
            )
            SystemPorts.clear_port(self.transport.serial.name)
        else:
            print("[connection_lost] Port closed")


class SystemPorts:
    _hosts: dict[str, Host] = {}
    _ports = {}
    _BAUD_RATE = 115200

    def get_ports_names():
        return SystemPorts._ports.keys()

    def init():
        SystemPorts._host = Host()
        for port_name in get_serial_ports():
            system_port = SystemPorts.get(port_name)
            if not system_port:
                SystemPorts.add(port_name)

    def add(port_name: str):
        if not SystemPorts.get_port(port_name):
            SystemPorts._ports[port_name] = PortReader()
            SystemPorts._ports[port_name].port = Serial(
                port=port_name, baudrate=SystemPorts._BAUD_RATE
            )

            if not SystemPorts.port_is_open(port_name):
                SystemPorts.get_port(port_name).open()

            SystemPorts._ports[port_name].reader = ReaderThread(
                SystemPorts.get_port(port_name), PrintLines
            )
            SystemPorts.get_reader(port_name).start()

    def get(port_name: str) -> PortReader:
        if port_name in SystemPorts._ports:
            return SystemPorts._ports[port_name]
        else:
            return None

    def get_port(port_name: str):
        if SystemPorts.get(port_name):
            return SystemPorts.get(port_name).port
        else:
            return None

    def get_reader(port_name: str):
        return SystemPorts.get(port_name).reader

    def clear_port(port_name: str):
        SystemPorts._ports[port_name] = None

    def close_port(port_name: str):
        if SystemPorts.get_port(port_name):
            SystemPorts.get_port(port_name).close()

    def close_all_ports():
        for port_name in SystemPorts.get_ports_names():
            SystemPorts.close_port(port_name)

    def port_is_open(port_name: str) -> bool:
        return SystemPorts.get_port(port_name).is_open

    def open_port(port_name: str):
        SystemPorts.get_port(port_name).open()

    def refresh():
        port_names = get_serial_ports()
        if len(port_names - SystemPorts.get_ports_names()) != 0:
            print("Ports changed: {}".format(port_names))
            SystemPorts.init()
