from serial import Serial
from serial.threaded import ReaderThread, LineReader
from utils import get_serial_ports, list_diff
from parser import get_points, get_mac_address, get_ssid, get_password, get_id, get_channel

class PortReader():
    port = None
    reader = None


class Host():
    channel = None
    id = None
    mac_address = None
    ssid = None
    password = None


    def set_id(self, id):
        self.id = id

    def set_channel(self, channel):
        self.channel = channel

    def set_mac_address(self, mac_address):
        self.mac_address = mac_address

    def set_ssid(self, ssid):
        self.ssid = ssid

    def set_password(self, password):
        self.password = password


class Teams():
    red = 0
    green = 0
    blue = 0


class Game():
    points: Teams = {}
    hosts: dict[str, Host] = {}

    def __init__(self, points = Teams(), hosts = {}):
        self.points = points
        self.hosts = hosts

class PrintLines(LineReader):
    def connection_made(self, transport):
        super(PrintLines, self).connection_made(transport)
        print("[connection_made] Connected, ready to receive data...")

    def handle_line(self, line):
        try:
            # print("[handle_line] New line: {}".format(line))
            points = get_points(line)
            if len(points) > 0:
                if SystemPorts._game.points.red == 0 and points[0][0] != 0:
                    SystemPorts._game.points.red = points[0][0]
                if SystemPorts._game.points.green == 0 and points[0][1] != 0:
                    SystemPorts._game.points.green = points[0][1]
                if SystemPorts._game.points.blue == 0 and points[0][2] != 0:
                    SystemPorts._game.points.blue = points[0][2]
                print("score updated: [R: {}, G: {}, B: {}]".format(points[0][0], points[0][1], points[0][2]))
                print(SystemPorts._game.points.__dict__)



            ids = get_id(line)
            if len(ids) > 0:
                id = ids[0]

                if not id in SystemPorts._game.hosts:
                    SystemPorts._game.hosts[id] = Host()
                    SystemPorts._game.hosts[id].set_id(id)

                    ssid = get_ssid(line)
                    if len(ssid) > 0:
                        SystemPorts._game.hosts[id].set_ssid(ssid[0])

                    password = get_password(line)
                    if len(password) > 0:
                        SystemPorts._game.hosts[id].set_password(password[0])

                    channel = get_channel(line)
                    if len(channel) > 0:
                        SystemPorts._game.hosts[id].set_channel(channel[0])

                    mac_address = get_mac_address(line)
                    if len(mac_address) > 0:
                        SystemPorts._game.hosts[id].set_mac_address(mac_address[0])

                print(SystemPorts._game.hosts['14'].__dict__)

        except Exception as exc:
            print("Exception: {}".format(exc))


    def connection_lost(self, exc):
        if self.transport.serial:
            print("[connection_lost] Port: [{}] closed".format(self.transport.serial.name))
            SystemPorts.clear_port(self.transport.serial.name)
        else:
            print("[connection_lost] Port closed")


class SystemPorts():
    _game: Game = {}
    _ports = {}
    _BAUD_RATE = 115200

    def get_ports_names():
        return SystemPorts._ports.keys()


    def init():
        SystemPorts._game = Game()
        for port_name in get_serial_ports():
            system_port = SystemPorts.get(port_name)
            if not system_port:
                SystemPorts.add(port_name)


    def add(port_name: str):
        if not SystemPorts.get_port(port_name):
            SystemPorts._ports[port_name] = PortReader()
            SystemPorts._ports[port_name].port = Serial(port=port_name, baudrate=SystemPorts._BAUD_RATE)

            if not SystemPorts.port_is_open(port_name):
                SystemPorts.get_port(port_name).open()

            SystemPorts._ports[port_name].reader = ReaderThread(SystemPorts.get_port(port_name), PrintLines)
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

