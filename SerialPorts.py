import sys
import glob
import serial

# This class is responsable for the serial port
class SerialPorts:
    # return the serials ports
    def serial_ports():
        ports = glob.glob('/dev/tty[A-Za-z]*')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except serial.SerialException:
                return 0
        port = "'" + result[0] + "'"
        return port
    
    # open serial port
    def open_serial():
        try:
            ser = serial.Serial('/dev/tty.usbserial-110', 115200, timeout=2)
            # ser = serial.Serial(serial_ports(), 115200)
        except serial.SerialException:
            return 0
        return ser
    
    # close serial port
    def close_serial(ser: serial):
        try:
            ser.close() 
        except serial.SerialException:
            return 0
        return 1