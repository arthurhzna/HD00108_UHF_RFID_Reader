# UHF RFID Reader Serial

Python service for reading UHF RFID tags through a serial connection and publishing device status plus RFID tag summaries through MQTT.

The reader/protocol reference is stored locally in this repository:

```text
UHF-RFID-Reader-Serial-User-Manual-V2.20.pdf
```

The current RFID implementation is located at:

```text
src/infrastructure/rfid/uhf_rfid.py
```

## Current Features

The RFID integration currently implements only 2 features:

1. `set_rf_power_to_max()`
   - Sends a serial command to set the reader RF power to the maximum configured value.
   - Called during RFID bootstrap.

2. `inventory()`
   - Sends the inventory command to the reader.
   - Reads the reader response.
   - Extracts EPC values from inventory response frames.
   - Returns EPC values as uppercase hexadecimal strings.

Other UHF RFID reader features from the manual are not implemented yet.

## How It Works

When the application starts:

1. Runtime configuration is loaded from `.env`.
2. The serial client opens a connection to the UHF RFID reader.
3. The MQTT client connects to the broker.
4. The reader RF power is set to maximum.
5. The scheduler polls RFID tags every `0.1` seconds.
6. Every 1 second, the application:
   - publishes device register/status data through MQTT;
   - publishes a summary of RFID tags read during the current cycle;
   - clears the temporary card state for the next cycle.

Read tags are stored temporarily in a set, so the same EPC is not duplicated within one publish cycle.

## Requirements

- Python `>= 3.12`
- UHF RFID reader with serial protocol support according to `UHF-RFID-Reader-Serial-User-Manual-V2.20.pdf`
- Serial/USB connection to the reader
- MQTT broker

Python dependencies:

- `pyserial`
- `paho-mqtt`
- `python-dotenv`

## Setup

Create your `.env` file from the example file first:

```bash
cp .env.example .env
```

Then edit `.env` and fill in the values for your device, serial port, and MQTT broker.

Example `.env.example` format:

```env
# ==========================
# Device
# ==========================
DEVICE_ID={}

# ==========================
# Serial
# ==========================
SERIAL_PORT=/dev/ttyUSB0
SERIAL_BAUDRATE=57600
SERIAL_TIMEOUT=1.0
SERIAL_RECONNECT=true

# ==========================
# MQTT
# ==========================
MQTT_BROKER={}
MQTT_PORT={}
MQTT_USERNAME={}
MQTT_PASSWORD={}
MQTT_USE_TLS={}
```

Install dependencies with `uv`:

```bash
uv sync
```

Or with a standard virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install paho-mqtt pyserial python-dotenv
```

## Configuration

### Device Variables

| Name | Code Default | Description |
| --- | --- | --- |
| `DEVICE_ID` | `ini_rfid_scanner` | Device ID used in MQTT payloads and subscribe topic. |
| `SOFTWARE_VERSION` | `1.0.0` | Software version sent in device status payloads. This variable is supported by the code but is not currently listed in `.env.example`. |

### Serial Variables

| Name | Code Default | Description |
| --- | --- | --- |
| `SERIAL_PORT` | empty | Reader serial port. Must be configured before the app can connect to the reader. |
| `SERIAL_BAUDRATE` | `115200` | Serial baudrate. The current `.env.example` uses `57600`; use the value that matches your reader configuration. |
| `SERIAL_TIMEOUT` | `1.0` | Serial read timeout in seconds. |
| `SERIAL_RECONNECT` | `true` | If `true`, the serial client tries to reconnect during read/write operations. |

Common serial port examples:

- macOS: `/dev/tty.usbserial-0001`, `/dev/tty.usbmodemXXXX`
- Linux: `/dev/ttyUSB0`, `/dev/ttyACM0`
- Windows: `COM3`, `COM4`

### MQTT Variables

| Name | Code Default | Description |
| --- | --- | --- |
| `MQTT_BROKER` | `localhost` | MQTT broker host. |
| `MQTT_PORT` | `1883` | MQTT broker port. |
| `MQTT_USERNAME` | empty | MQTT username, if authentication is required. |
| `MQTT_PASSWORD` | empty | MQTT password. |
| `MQTT_USE_TLS` | `false` | If `true`, the client enables TLS. |

`MQTT_CLIENT_ID` is not configured manually. The application generates it automatically with this format:

```text
<random_8_hex>_<DEVICE_ID>
```

## Running

With `uv`:

```bash
uv run python src/main.py
```

Or, if a virtual environment is already active:

```bash
python src/main.py
```

Stop the application with `Ctrl+C`.

## MQTT

### Subscribe Topic

The application subscribes to:

```text
echoscan/subscribe/<DEVICE_ID>
```

Supported incoming messages:

```json
{
  "action": "device_registered"
}
```

Effect: marks the device as registered. The next sync cycle will publish device status instead of a register message.

```json
{
  "action": "device_reset"
}
```

Effect: clears the device registration state. The application will publish a register message again.

### Register Publish Topic

Topic:

```text
echoscan/register
```

Payload:

```json
{
  "action": "device_register",
  "id": "ini_rfid_scanner",
  "timestamp": "2026-07-29T16:00:00"
}
```

### Data Publish Topic

Topic:

```text
echoscan/publish
```

Device status payload:

```json
{
  "action": "device_status",
  "id": "ini_rfid_scanner",
  "timestamp": "2026-07-29T16:00:00",
  "firmware_version": "1.0.0"
}
```

RFID summary payload:

```json
{
  "action": "rfid_summary",
  "id": "ini_rfid_scanner",
  "timestamp": "2026-07-29T16:00:00",
  "cards": [
    "E2000017221101441890ABCD"
  ]
}
```

## RFID Implementation

Main file:

```text
src/infrastructure/rfid/uhf_rfid.py
```

Serial command definitions:

```text
src/infrastructure/rfid/command.py
```

### Set RF Power To Maximum

Command:

```text
08 FF 2F 1E 1E 1E 1E 37 54
```

Used by:

```python
UHFRFID.set_rf_power_to_max()
```

This method sends the command to the reader and reads one response line. It returns `True` when a response is received, and `False` when write fails or no response is received.

### Inventory Tags

Command:

```text
09 FF 01 04 01 00 80 0A 3C 48
```

Used by:

```python
UHFRFID.inventory()
```

This method:

1. Sends the inventory command to the reader.
2. Reads up to `512` bytes from the serial response.
3. Passes the response to the parser.
4. Returns a list of EPC tag values.

Parser:

```text
src/infrastructure/rfid/parser.py
```

The parser reads response frames using the current implementation rules:

- the first byte is the frame length;
- inventory frames are accepted when `frame[2] == 0x01`;
- EPC length is read from `frame[6]`;
- EPC bytes are read from `frame[7:7 + epc_length]`;
- EPC values are returned as uppercase hex strings.

## Project Structure

```text
src/
  main.py                         Application entry point
  bootstrap/                      Application dependency wiring
  config/                         .env configuration loaders
  domain/service/                 Domain service interfaces
  application/
    scheduler/                    Scheduler loop and interval triggers
    state/                        Temporary device and card state
    usecase/                      Device and RFID use cases
  infrastructure/
    rfid/                         UHF RFID serial implementation
    serial/                       pyserial wrapper
    messaging/mqtt/               MQTT client, publisher, and payloads
    serializer/                   JSON serializer
    time/                         System clock
  presentation/messaging/         MQTT message router and incoming handlers
```

## Troubleshooting

### Serial Does Not Connect

- Make sure `SERIAL_PORT` is set.
- Make sure the reader is connected and the selected port is correct.
- Make sure the current user has permission to access the serial port.
- Check that `SERIAL_BAUDRATE` matches the reader configuration.

### No Tags Are Read

- Make sure the tag is within the reader range.
- Make sure the reader antenna is connected.
- Make sure the reader has enough power.
- Check that the inventory command matches the reader model and manual.

### MQTT Does Not Publish

- The application skips publishing while MQTT is not connected.
- Make sure `MQTT_BROKER` and `MQTT_PORT` are correct.
- If the broker requires authentication, set `MQTT_USERNAME` and `MQTT_PASSWORD`.
- If the broker requires TLS, set `MQTT_USE_TLS=true`.

## Development Notes

- Add new RFID features in `src/infrastructure/rfid/uhf_rfid.py`.
- Store new command bytes in `src/infrastructure/rfid/command.py`.
- If a new command has a different response format, add parser logic in `src/infrastructure/rfid/parser.py`.
- Match command bytes, parameters, and response formats with `UHF-RFID-Reader-Serial-User-Manual-V2.20.pdf`.
- Parser tests are recommended when adding RFID features because response frame handling is the most protocol-sensitive part of the implementation.
