import re

points = r'^Chicken\s(\d{1,2})\:\s(\d+)\,(\d+)\,(\d+)$'
mac_address = r'MAC\-Address\:\s{3}(\d{,2}[ABCDEF]{,2}\:\d{,2}[ABCDEF]{,2}\:\d{,2}[ABCDEF]{,2}\:\d{,2}[ABCDEF]{,2}\:\d{,2}[ABCDEF]{,2}\:\d{,2}[ABCDEF]{,2})'
ssid = r'SSID:\s{10}(Chicken_(Easy|Medium|Hard)_\d{1,2})\n'
password = r'Password:\s{6}(.*)\n'
id = r'Chicken ID:\s{4}([0-9]{2})\n'
channel = r'Channel:\s{6,7}(\d{1,2})\n'

def match(text: str, rgex):
    return re.findall(rgex, text)


def get_points(text: str):
    return match(text, points)


def get_mac_address(text: str):
    return match(text, mac_address)


def get_ssid(text: str):
    return match(text, ssid)


def get_password(text: str):
    return match(text, password)


def get_id(text: str):
    return match(text, id)


def get_channel(text: str):
    return match(text, channel)
