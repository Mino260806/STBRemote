from actions import Action
from listener.base import Listener

import serial
import serial.tools.list_ports

from listener.raw.starsat import STARSAT_CODES


class SerialListener(Listener):
    def listen(self):
        ports = serial.tools.list_ports.comports()

        selected_port = None
        for port, desc, hwid in ports:
            print("{}: {} [{}]".format(port, desc, hwid))
            selected_port = port

        ser = serial.Serial(selected_port, 9600, timeout=1)

        while True:
            if ser.isOpen():
                input_data = ser.readline().strip().decode("utf-8")
                try:
                    ir_code = int(input_data, 16)
                    self.handle_ir_code(ir_code)
                except ValueError:
                    pass

    def handle_ir_code(self, ir_code):
        pass


class StarsatSerialListener(SerialListener):
    def handle_ir_code(self, ir_code):
        action = STARSAT_CODES.get(ir_code)
        print(hex(ir_code), action)
        if isinstance(action, Action):
            self.dispatch_action(action)
