from enum import IntEnum


class EventType(IntEnum):
    INSERT = 0x01
    DELETE = 0x02
    HIGHLIGHT = 0x03
    COMMENT = 0x04
    CURSOR_MOVE = 0x05
    SEEK_REQUEST = 0x10
    PAUSE_REPLAY = 0x11
    RESUME_REPLAY = 0x12
    JUMP_TO_END = 0x14
    SYNC = 0xFE
    PING = 0xFF
