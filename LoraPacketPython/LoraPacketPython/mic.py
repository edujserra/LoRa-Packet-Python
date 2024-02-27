from LoraPacketPython.LoraPacketPython.LoraPacket import LoraPacket, reverseBuffer
from cryptography.hazmat.primitives import cmac
from cryptography.hazmat.primitives.ciphers import algorithms


def calculateMIC(
    payload: LoraPacket,
    NwkSKey: bytes,
):
    if NwkSKey and len(NwkSKey) != 16:
        return None
    if payload.DevAddr and len(payload.DevAddr) != 4:
        return None
    if payload.FCnt and len(payload.FCnt) != 2:
        return None
    if not payload.MHDR:
        return None
    if not payload.DevAddr:
        return None
    if not payload.FCnt:
        return None
    if not payload.MACPayload:
        return None

    FCntMSBytes = bytes.fromhex("0000")

    if payload.getDir() != "up":
        return None

    dir = bytes(bytearray(1))

    msgLen = len(payload.MHDR) + len(payload.MACPayload)

    B0 = (
        bytes.fromhex("49")
        + bytes(bytearray(4))
        + dir
        + reverseBuffer(payload.DevAddr)
        + reverseBuffer(payload.FCnt)
        + FCntMSBytes
        + bytes(bytearray(1))
        + bytes(bytearray([msgLen]))
    )

    # CMAC over B0 | MHDR | MACPayload
    cmacInput = bytes(B0 + payload.MHDR + payload.MACPayload)

    # CMAC calculation (as RFC4493)
    key = NwkSKey

    c = cmac.CMAC(algorithms.AES(key))
    c.update(cmacInput)

    fullCmac = c.finalize()

    # only first 4 bytes of CMAC are used as MIC
    MIC = fullCmac[0:4]

    return MIC


def verifyMIC(payload: LoraPacket, NwkSKey: bytes):
    if payload.MIC and len(payload.MIC) != 4:
        return False

    calculated = calculateMIC(payload, NwkSKey)

    if not payload.MIC:
        return False

    return payload.MIC == calculated
