from threading import Thread, Event

from system_ports import SystemPorts
from thread_handlers import handle_ports, handle_get_points, handle_input
import ws_service

if __name__ == "__main__":
    try:
        ports_event = Event()
        points_event = Event()
        input_event = Event()

        # get the system serial ports
        SystemPorts.init()

        thread_ports = Thread(target=handle_ports, args=(ports_event,))
        thread_points = Thread(target=handle_get_points, args=(points_event,))
        thread_input = Thread(target=handle_input, args=(input_event,))

        thread_ports.start()
        thread_points.start()
        thread_input.start()

        ws_service.server.run_forever()

        while True:
            pass

    except (KeyboardInterrupt, SystemExit):
        print("Interrupted!")
    finally:
        ports_event.set()
        points_event.set()
        input_event.set()

        thread_ports.join()
        thread_points.join()
        thread_input.join()

        SystemPorts.close_all_ports()

        ws_service.server.shutdown_gracefully()

        print("Script terminated")
