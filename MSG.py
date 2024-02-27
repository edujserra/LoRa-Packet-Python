import serial
import time

# Mensagem CSTDN:port:size:msg_counter\r\n 

ERRO = '300\r\n' # erro sending message or message queue full in C-Point
INQUEUE = '400\r\n' # message in queue
SENT = '500\r\n' # message prepared for sending
SENT_ACK = '600\r\n' # message sent

command_cmesh = "CMESH:"
command_cstdn = "CSTDN:"

class MSG:
    def cmesh_msg(msg: str):
        return command_cmesh + msg + '\r\n'

    def cstdn_msg(msg: str, port: int, size: int, msg_counter: int):
        return command_cstdn + port + ':' + str(size) + ':' + str(msg_counter) + ':' + msg + '\r\n'

    def send_serial(msg: str, ser: serial):
        try:
            ser.write(msg.encode("utf-8"))
        except serial.SerialException:
            return 0
        time.sleep(0.5)
        return 1

    def send_msg(msg: str, ser: serial):
        while True:
            retval = MSG.send_serial(msg, ser)

            if retval == 0:
                return 0
            
            received_data = ser.readline()
            if received_data:
                decode_data = received_data.decode("utf-8")

                parts = decode_data.split(":")
                fport = parts[1]

                if (fport == INQUEUE):
                    return 1
                elif (fport == ERRO):
                    time.sleep(10)
                else:
                    time.sleep(1)
            
    