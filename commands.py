import system_ports

CHICKENS_PWD = "edfd8e8160383696120dfb444a8b43f1"


def convert(command: str):
    encoded = command.encode("utf-8")
    return bytearray(encoded)


def get_all_points():
    cmd = convert("points")
    for port_name in system_ports.SystemPorts.get_ports_names():
        if system_ports.SystemPorts.get_port(port_name):
            system_ports.SystemPorts.get_port(port_name).write(cmd)


def reset_all():
    cmd = convert("reset -p {}".fotmat(CHICKENS_PWD))
    for port_name in system_ports.SystemPorts.get_ports_names():
        if system_ports.SystemPorts.get_port(port_name):
            system_ports.SystemPorts.get_port(port_name).write(cmd)
