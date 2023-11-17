from serial.tools import list_ports


def get_serial_ports():
    ports = list_ports.grep(r"^.*(usb|COM[0-9]+).*$")

    result = []
    for port, _, _ in sorted(ports):
        result.append(port)

    return result


def print_all(obj: object):
    for attr in dir(obj):
        print("{}: {}".format(attr, getattr(obj, attr)))


def list_diff(list1, list2):
    diff = []

    for element in list1:
        if element not in list2:
            diff.append(element)

    return diff
