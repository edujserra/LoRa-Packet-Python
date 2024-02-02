import base64
from LoraPacket import LoraPacket
from crypto import loramac_decrypt
from mic import calculateMIC, verifyMIC


def decode(b64_data: str, nwkKey: str, appKey: str):
    input_buffer = base64.b64decode(b64_data)
    appKey = bytes.fromhex(appKey)
    nwkKey = bytes.fromhex(nwkKey)

    packet = LoraPacket(input_buffer)
    print(packet.__str__())

    micOk = (
        " (OK)"
        if verifyMIC(packet, nwkKey)
        else " (BAD != " + calculateMIC(packet, nwkKey).hex() + ")"
    )

    print(f"        MIC State: {micOk}")

    decipher_key = bytes(nwkKey if packet.getFPort() == 0 else appKey)

    plain_buffer = bytearray(
        loramac_decrypt(
            packet.FRMPayload.hex(),
            packet.getFCnt(),
            decipher_key.hex(),
            packet.DevAddr.hex(),
        )
    )

    plain_text = plain_buffer.decode("utf-8")

    print(f"        Decoded payload: {plain_text}")


if __name__ == "__main__":
    DATA = "QK8CCyYAAQACngFTe003RTA="
    NWK_KEY = "87F1802E0C803DEB919F93814596345E"
    APP_KEY = "067469A70DFFF46C84ED6756DB5FFDFB"

    decode(DATA, NWK_KEY, APP_KEY)
