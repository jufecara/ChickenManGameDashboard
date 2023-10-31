class Teams():
    red = 0
    green = 0
    blue = 0

class Host():
    channel = None
    id = None
    mac_address = None
    ssid = None
    password = None
    points: Teams = None


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

    def set_points(self, points):
        self.points = points
