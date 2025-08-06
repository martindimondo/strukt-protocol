import struct


def pack_tlv(event_type: int, payload: bytes) -> bytes:
    return struct.pack(">BH", event_type, len(payload)) + payload


def unpack_tlv(data: bytes):
    event_type, length = struct.unpack(">BH", data[:3])
    payload = data[3 : 3 + length]
    return event_type, payload
