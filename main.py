import sqlite3
import serial
from LoraPacketPython.LoraPacketPython.main import decode
from MSG import MSG
from SQL import SQL
from SerialPorts import SerialPorts

# DevAddr test
DevAddr_test = '260B02AF'
FPort = ' 15'

def main_func(conn: sqlite3, ser: serial, DevAddr: str, payload: str):
    cur = conn.cursor()
    sql_command = '''SELECT * FROM device WHERE DevAddr = ? '''

    # SQLite rows DevAddr, NwkKey, AppKey
    res = cur.execute(sql_command, (DevAddr,)).fetchone()

    if res:
        if res[1] == None and res[2] == None:
            size_text = len(payload)
            msg_CSTDN = MSG.cstdn_msg(payload, 0, size_text, 0)
            MSG.send_msg(msg_CSTDN, ser)

        if res[1] != None and res[2] != None:
            mickOk, plainText, FCnt = decode(payload, res[2], res[1])

            # print("FCnt: " + str(FCnt))
            
            if mickOk == " (OK)":
                plainText = plainText.decode("utf-8")
                # update BD
                # Coordinates and battery using the plaintext
                coordinates = plainText
                battery = 100

                sql_command = '''SELECT DevAddr FROM buoyStatus WHERE DevAddr = ? '''
                res = cur.execute(sql_command, (DevAddr,)).fetchone()
                if res:
                    SQL.update_buoyStatus(conn, DevAddr, coordinates, battery)
                else:
                    SQL.insert_table_buoy(conn, DevAddr, coordinates, battery)

                msg_CMESH = MSG.cmesh_msg(plainText)
                size_text = len(plainText)
                MSG.send_msg(msg_CMESH, ser)
                
                msg_CSTDN = MSG.cstdn_msg(payload, FPort, size_text, 0)
                MSG.send_msg(msg_CSTDN, ser)
    
    cur.close()

if __name__ == "__main__":
    conn = SQL.create_connection('ex1.db')
    ser = SerialPorts.open_serial()
    main_func(conn, ser, DevAddr_test, 'QK8CCyYAAQACngFTe003RTA=')










