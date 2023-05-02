import time
import serial
import atexit

from serial.tools import list_ports


class Communication:
    serial_connection = None

    def __init__(self, baud_rate):
        self.handshake(baud_rate)

    def get_message(self):
        message = self.serial_connection.readline().decode("utf-8").rstrip()
        return message

    def send_message(self, message):
        if self.serial_connection.isOpen():
            self.serial_connection.write(message.encode("ascii"))
            self.serial_connection.flush()

    def exit_handler(self):
        self.serial_connection.close()

    def handshake(self, baud_rate):
        found = False
        while not found:
            for com in list(list_ports.comports()):
                if "ARDUINO" in str(com).upper():
                    print("TESTING: ", com)
                    com_port = str(com).split(" ")[0]
                    try:
                        self.serial_connection = serial.Serial(com_port,
                                                               baudrate=baud_rate,
                                                               timeout=2.5,
                                                               parity=serial.PARITY_NONE,
                                                               bytesize=serial.EIGHTBITS,
                                                               stopbits=serial.STOPBITS_ONE)
                        time.sleep(2)
                        message = "BURGLAR CONNECTION REMOTE"
                        self.send_message(message)
                        response = self.get_message()
                        if type(response) is str:
                            if response == "BURGLAR CONNECTION LOCAL":
                                print("Arduino Found")
                                atexit.register(self.exit_handler)
                                found = True
                            else:
                                self.serial_connection.close()
                                print("NOT SAME")
                    except serial.serialutil.SerialException:
                        print("ACCESS DENIED")
            if not found:
                print("Arduino not found")
                exit(0)
