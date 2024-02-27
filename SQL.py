import sqlite3
from sqlite3 import Error
import datetime

"""
Table to store device address, and respective application and 
                    network keys, if they exits.
        DevAddr : Device Address
        AppKey : Application Key
        NwkKey : Network Key """

table_device = '''CREATE TABLE device(
                    DevAddr     CHAR(8)  PRIMARY KEY,
                    AppKey      CHAR(32),
                    NwkKey      CHAR(32));'''

"""
Table to store informations from known devices.
        DevAddr : Device Address
        Coordinates : Coordinates
        Battery : Battery level from the buoy
        Date_time : YYYY-MM-DD HH:MM:SS.ssssss """
  
table_buoy = '''CREATE TABLE buoyStatus(
                    DevAddr         CHAR(8)  PRIMARY KEY,
                    Coordinates     TEXT    NOT NULL,
                    Battery         INT     NOT NULL,
                    Date_time       TEXT    NOT NULL);'''

class SQL:
    # Used for create a connection
    def create_connection(db_file: str):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            return None

        return conn

    # Used for creating the 2 tables, device and buoyStatus
    def create_table(conn: sqlite3):
        try:
            cursor = conn.cursor()
            cursor.execute('''DROP TABLE IF EXISTS device''')
            cursor.execute('''DROP TABLE IF EXISTS buoyStatus''')

            cursor.execute(table_device)
            cursor.execute(table_buoy)
        
            conn.commit()
            cursor.close()
        except Error as e:
            return 0
        
        return 1
    
    # Used for inserting in the table device, the keys for a known device
    def insert_table_device(conn: sqlite3, DevAddr: str, AppKey: str, NwkKey: str):            
        try:
            cursor = conn.cursor()

            if AppKey == "" and NwkKey == "":
                sql_command = '''INSERT INTO device (DevAddr) VALUES (?);'''
                cursor.execute(sql_command, (DevAddr,))
            else:
                sql_command = '''INSERT INTO device (DevAddr, AppKey, NwkKey) VALUES (?, ?, ?);'''
                cursor.execute(sql_command, (DevAddr, AppKey, NwkKey))

            conn.commit()
            cursor.close()
        except Error as e:
            return 0
        
        return 1

    # Used for inserting in the table buoyStatus, the information received from a known device
    def insert_table_buoy(conn: sqlite3, DevAddr: str, coordinates: str, battery: int):
        currentDateTime = currentDateTime = datetime.datetime.now()
        sql_command  = '''INSERT INTO buoyStatus (DevAddr, Coordinates, battery, Date_time) VALUES (?, ?, ?, ?);'''

        try:
            cursor = conn.cursor()
            cursor.execute(sql_command, (DevAddr, coordinates, battery, currentDateTime))

            conn.commit()
            cursor.close()
        except Error as e:
            return 0
        
        return 1

    # Used for updating the device table, updating the AppKey and Nwkkey for a already existing DevAddr
    def update_device(conn: sqlite3, DevAddr: str, AppKey: str, NwkKey: str):
        sql_command = ''' UPDATE device
                            SET AppKey = ? ,
                                NwkKey = ? 
                            WHERE DevAddr = ?'''
        try:
            cursor = conn.cursor()
            cursor.execute(sql_command, (AppKey, NwkKey, DevAddr))

            conn.commit()
            cursor.close()
        except Error as e:
            return 0
        
        return 1

    # Used for updating the buoyStatus, updating the coordinates, battery level and current time for a
    # already existing DevAddr
    def update_buoyStatus(conn: sqlite3, DevAddr: str, coordinates: str, battery: int):
        currentDateTime = currentDateTime = datetime.datetime.now()
        sql_command = ''' UPDATE buoyStatus
                            SET Coordinates = ? ,
                                Battery = ? ,
                                Date_Time = ? 
                            WHERE DevAddr = ?'''
    
        try:
            cursor = conn.cursor()
            cursor.execute(sql_command, (coordinates, currentDateTime, battery, DevAddr))

            conn.commit()
            cursor.close()
        except Error as e:
            return 0

        return 1
    
    # Used for deleting a device from the device table
    def delete_device(conn: sqlite3, DevAddr: str):
        sql_command = '''DELETE FROM device WHERE DevAddr = ?'''
        
        try:
            cursor = conn.cursor()
            cursor.execute(sql_command, (DevAddr))

            conn.commit()
            cursor.close()
        except Error as e:
            return 0

        return 1

    # Used for deleting the information of a buoy from the buoyStatus table
    def delete_buoyStatus(conn: sqlite3, DevAddr: str):
        sql_command = '''DELETE FROM buoyStatus WHERE DevAddr = ?'''

        try:
            cursor = conn.cursor()
            cursor.execute(sql_command, (DevAddr))

            conn.commit()
            cursor.close()
        except Error as e:
            return 0
        
        return 1

        