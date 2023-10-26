
import serial.tools.list_ports

def get_serial_ports():
    ports = serial.tools.list_ports.comports()
    
    result = []
    for port, _, _ in sorted(ports):
        result.append(port)

    return result


if __name__ == '__main__':
    print("{}".format(get_serial_ports()))
