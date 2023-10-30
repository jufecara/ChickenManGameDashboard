from serial.tools import list_ports

def get_serial_ports():
    ports = list_ports.grep(r'^.*usb.*$')

    result = []
    for port, _, _ in sorted(ports):
        result.append(port)

    return result


def print_all(obj: object):
    for attr in dir(obj):
        print("{}: {}".format(attr, getattr(obj, attr)))
