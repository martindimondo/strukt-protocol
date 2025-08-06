from strukt.codec import pack_tlv, unpack_tlv
from strukt.events import InsertEvent
from strukt.protocol import EventType


def test_pack_and_unpack_tlv():
    payload = b"hello"
    event_type = EventType.INSERT
    frame = pack_tlv(event_type, payload)

    decoded_type, decoded_payload = unpack_tlv(frame)
    assert decoded_type == event_type
    assert decoded_payload == payload


def test_insert_event_encoding():
    event = InsertEvent(timestamp=1_000_000, line=2, column=5, text="hello")
    encoded = event.encode()
    decoded = InsertEvent.decode(encoded)

    assert decoded.timestamp == event.timestamp
    assert decoded.line == event.line
    assert decoded.column == event.column
    assert decoded.text == event.text


def test_full_encode_decode_cycle():
    event = InsertEvent(timestamp=1_000_000, line=0, column=0, text="test123")
    encoded_payload = event.encode()
    frame = pack_tlv(EventType.INSERT, encoded_payload)

    decoded_type, decoded_payload = unpack_tlv(frame)
    assert decoded_type == EventType.INSERT

    decoded_event = InsertEvent.decode(decoded_payload)
    assert decoded_event.text == "test123"
    assert decoded_event.timestamp == 1_000_000
