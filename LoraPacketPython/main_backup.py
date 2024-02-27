# This is a sample Python script.
import socket
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from datetime import datetime
from gpsdclient import GPSDClient
from lora.crypto import loramac_decrypt
from LoraPacketPython.main import decode
import json
import base64
import struct

# Press the green button in the gutter to run the script.
def main():


    localIP = "0.0.0.0"

    localPort = 1700

    bufferSize = 1024

    msgFromServer = "Hello UDP Client"

    bytesToSend = str.encode(msgFromServer)

    # Create a datagram socket

    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Bind to address and ip

    UDPServerSocket.bind((localIP, localPort))

    print("UDP server up and listening")

    # Listen for incoming datagrams

    while (True):
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        now = datetime.now()
        message = bytesAddressPair[0]

        address = bytesAddressPair[1]
        clientMsg = "Message from Client:{}".format(message)
        clientIP = "Client IP Address:{}".format(address)

        if "rxpk" in str(message) or "stat" in str(message):
                with GPSDClient(host="127.0.0.1") as client:
                        lat = 0
                        lon = 0
                        for result in client.dict_stream(convert_datetime=True, filter=["TPV"]):
                                print("Latitude: %s" % result.get("lat", "n/a"))
                                print("Longitude: %s" % result.get("lon", "n/a"))
                                lat = result.get("lat", "n/a")
                                lon = result.get("lon", "n/a")
                                break

                        # Decode the byte string into a regular string
                        decoded_sentence = message.decode('latin-1')

                        # Find the index of the first '{' character
                        json_start_index = decoded_sentence.find('{')

                        # Extract the JSON string
                        json_string = decoded_sentence[json_start_index:]

                        # Parse the JSON string into a dictionary
                        parsed_json = json.loads(json_string)
                        data = ""
                        devAddr = ""
                        if "rxpk" in str(message):
                               for elem in parsed_json["rxpk"]:
                                       data = elem["data"]
                                       devAddr = ""
                                       decoded_payload = base64.b64decode(elem["data"])
                                       devAddr = struct.unpack('<I', decoded_payload[1:5])[0]
                                       # file1 = open("data.txt", "a")  # append mode
                                       # file1.write("{\"type\":\"rxpk\",\"date\":\"" + str(now) + "\",\"message\":\"" + str(parsed_json) + "\",\"devAddr\":\"" + str(hex(devAddr)) + "\",\"data\":\"" + str(data) + "\",\"lat\":\"" + str(lat) + "\",\"lon\":\"" + str(lon) + "\"}\n")
                                       # file1.close()
                        # else:
                               # file1 = open("data.txt", "a")  # append mode
                               # file1.write("{\"type\":\"stat\",\"date\":\"" + str(now) + "\",\"message\":\"" + str(parsed_json) + "\",\"lat\":\"" + str(lat) + "\",\"lon\":\"" + str(lon) + "\"}\n")
                               # file1.close()
                        # print("Data saved!")
        else:
                print("No Data!")
        print(clientMsg)
        print(clientIP)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

try:
    while True:
        main()
except Exception as e:
    pass
