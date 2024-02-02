from enum import IntEnum
import struct


class MType(IntEnum):
    JOIN_REQUEST = 0
    JOIN_ACCEPT = 1
    UNCONFIRMED_DATA_UP = 2
    UNCONFIRMED_DATA_DOWN = 3
    CONFIRMED_DATA_UP = 4
    CONFIRMED_DATA_DOWN = 5
    REJOIN_REQUEST = 6


def reverseBuffer(byte_obj):
    return byte_obj[::-1]


def readUInt8(data, offset: int):
    return struct.unpack("B", data[offset : offset + 1])[0]


def readInt8(data, offset):
    return struct.unpack("b", data[offset : offset + 1])[0]


def readUInt16BE(data, offset):
    return struct.unpack(">H", data[offset : offset + 2])[0]


def writeUInt8(buffer: bytes, value, offset: int):
    struct.pack_into("B", buffer, offset, value)


class LoraPacket:
    def __init__(self, buffer: bytes) -> None:
        incoming = bytes(buffer)

        self.PHYPayload = incoming
        self.MHDR = incoming[0:1]
        self.MACPayload = incoming[1 : len(incoming) - 4]
        self.MACPayloadWithMIC = incoming[1 : len(incoming)]
        self.MIC = incoming[len(incoming) - 4 :]

        if self.isDataMessage():
            # Decode message packet
            self.DevAddr = reverseBuffer(incoming[1:5])
            self.FCtrl = reverseBuffer(incoming[5:6])
            self.FCnt = reverseBuffer(incoming[6:8])

            FCtrl = readInt8(self.FCtrl, 0)
            FOptsLen = FCtrl & 0x0F
            self.FOpts = incoming[8 : 8 + FOptsLen]

            FHDR_length = 7 + FOptsLen
            self.FHDR = incoming[1 : 1 + FHDR_length]

            if FHDR_length == len(self.MACPayload):
                self.FPort = bytes(bytearray())
                self.FRMPayload = bytes(bytearray())
            else:
                self.FPort = incoming[FHDR_length + 1 : FHDR_length + 2]
                self.FRMPayload = incoming[FHDR_length + 2 : len(incoming) - 4]

    def _getMType(self):
        if self.MHDR:
            return (readUInt8(self.MHDR, 0) & 0xFF) >> 5
        return -1

    def getDir(self):
        mType = self._getMType()
        if mType > 5:
            return None
        if mType % 2 == 0:
            return "up"
        return "down"

    def isDataMessage(self):
        mtype = self._getMType()
        return mtype >= MType.UNCONFIRMED_DATA_UP and mtype <= MType.CONFIRMED_DATA_DOWN

    def getFPort(self):
        if self.FPort and len(self.FPort):
            return readUInt8(self.FPort, 0)
        return None

    def getFCnt(self):
        if self.FCnt:
            return readUInt16BE(self.FCnt, 0)
        return None

    def __str__(self) -> str:
        return f"""
        PHYPayload = {self.PHYPayload.hex()}
        MHDR = {self.MHDR.hex()}
        MACPayload =  {self.MACPayload.hex()}
        MIC =  {self.MIC.hex()}
        DevAddr = {self.DevAddr.hex()}
        FCnt = {self.getFCnt()}
        """
