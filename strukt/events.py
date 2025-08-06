from dataclasses import dataclass
import struct


@dataclass
class InsertEvent:
    timestamp: int
    line: int
    column: int
    text: str

    def encode(self) -> bytes:
        text_bytes = self.text.encode("utf-8")
        payload = struct.pack(
            ">IHHH", self.timestamp, self.line, self.column, len(text_bytes)
        )
        return payload + text_bytes

    @classmethod
    def decode(cls, data: bytes):
        timestamp, line, col, length = struct.unpack(">IHHH", data[:10])
        text = data[10 : 10 + length].decode("utf-8")
        return cls(timestamp, line, col, text)
