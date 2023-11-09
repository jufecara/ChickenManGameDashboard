from websocket_server import WebsocketServer
from commands import reset_all

PORT = 8001


# Called when a client sends a message
def message_received(client, server, message):
    if message == "reset":
        print("[message_received] reseting devices")
        reset_all()


server = WebsocketServer(port=PORT)
server.set_fn_message_received(message_received)
