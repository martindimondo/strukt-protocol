# Strukt Protocol Specification

**Version:** 0.1 — August 2025
**Author:** Martín Dimondo
**License:** Apache 2.0

---

## 1. Overview

**Strukt** is a binary, event based protocol for structured rich text streaming. It is designed for low latency, full-duplex communication over transports such as WebSocket or TCP. Strukt enables code mentoring, and real-time session replay with high quality display

---

## 2. Design Goals

* Real-time streaming of structured text changes
* Minimal payload size via binary TLV encoding
* Metadata support (highlighting, cursors, authorship)
* Full-duplex, low-latency communication
* Seekable playback for replay and time-based navigation
* Transport-agnostic architecture

---

## 3. Transport Layer

Strukt is transport-agnostic but requires a full-duplex, ordered and reliable connection. Supported transports include:

* WebSocket (recommended)
* TCP

Each connection corresponds to a single streaming session.

---

## 4. TLV Format

Each message in Strukt follows a Type, Length, Value structure:

| Field  | Size     | Description                 
| ------ | -------- | --------------------------- 
| Type   | 1 byte   | Type of event (opcode)      
| Length | 2 bytes  | Length of the payload       
| Value  | Variable | Binary payload of the event 

Multiple TLV frames may be sent consecutively without extra headers.

---

## 5. Common Event Types

| Type Hex | Name         | Description                      |
| -------- | ------------ | -------------------------------- |
| 0x01     | Insert       | Insert text at a given position  |
| 0x02     | Delete       | Delete a text range              |
| 0x03     | Highlight    | Visual annotation of a range     |
| 0x04     | Comment      | Attach comment to text range     |
| 0x05     | CursorMove   | Update user cursor position      |
| 0x10     | SeekRequest  | Request replay from timestamp    |
| 0x11     | PauseReplay  | Pause replay session             |
| 0x12     | ResumeReplay | Resume replay session            |
| 0x14     | JumpToEnd    | Jump to latest known state       |
| 0xFE     | Sync         | Sync state snapshot at timestamp |
| 0xFF     | Ping/Pong    | Keepalive / latency check        |

---

## 6. Event: Insert (0x01)

Payload structure:

| Field       | Type   | Size | Description              |
| ----------- | ------ | ---- | ------------------------ |
| Timestamp   | uint32 | 4    | Milliseconds since epoch |
| Line        | uint16 | 2    | Line number              |
| Column      | uint16 | 2    | Column index             |
| Text Length | uint16 | 2    | Length of text inserted  |
| Text        | utf-8  | N    | Text content             |

---

## 7. Event: Sync (0xFE)

A snapshot of the document state at a given time.

| Field     | Type   | Size | Description                     |
| --------- | ------ | ---- | ------------------------------- |
| Timestamp | uint32 | 4    | Epoch timestamp of the snapshot |
| Flags     | uint8  | 1    | Bitmask for what is included    |
| Hash      | uint32 | 4    | Optional document hash          |
| Data      | bytes  | N    | Document body or delta (utf-8)  |

**Flags:**

* `0x01` = Full document included
* `0x02` = Delta from previous sync
* `0x04` = Cursor data present
* `0x08` = Metadata annotations present

---

## 8. Event: SeekRequest (0x10)

Sent by client to request stream starting from a given point in time.

| Field     | Type   | Size | Description                   |
| --------- | ------ | ---- | ----------------------------- |
| Timestamp | uint32 | 4    | Desired start time for replay |

Server responds with a `SYNC` followed by events >= timestamp.

---

## 9. Session Flow

### Live streaming:

1. Client connects via WebSocket
2. Client sends events (insert/delete/etc.) as TLV frames
3. Server relays to other clients

### Seeking replay:

1. Client connects and sends `SeekRequest(t)`
2. Server sends `SYNC(t)` to sync document
3. Server streams stored events from `t` forward

---

## 10. Extensibility

* Reserved type range `0x80-0xEF` for user-defined extensions
* Version negotiation may be embedded in `SYNC` or handshake
* Optional metadata can evolve without breaking base format

---

## 11. Security Considerations

* All transport should use TLS (e.g. `wss://`)
* Authentication may be layered on top (JWT, API keys)
* Input validation on all incoming TLVs
* Rate limiting and abuse detection


---

*End of Specification — v0.1*
