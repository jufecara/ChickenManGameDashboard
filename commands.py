from system import SystemPorts

def convert(command: str):
    encoded = command.encode("utf-8")
    return bytearray(encoded)

def get_all_points():
    cmd = convert("points")
    for port_name in SystemPorts.get_ports_names():
        SystemPorts.get(port_name).port.write(cmd)


def reset_all():
    cmd = convert("reset -p edfd8e8160383696120dfb444a8b43f1")
    for port_name in SystemPorts.get_ports_names():
        SystemPorts.get(port_name).port.write(cmd)
