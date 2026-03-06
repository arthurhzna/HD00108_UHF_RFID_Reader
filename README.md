## UHF RFID Integration

This repository contains a Python-based service for integrating a UHF RFID reader with external systems over MQTT. 
It connects to a UHF RFID reader via a serial port, manages RF power and tag inventory, and publishes events (such as device status and tag summaries) through an internal event bus and MQTT.

### Features

- **Serial connection to UHF RFID reader** using `pyserial`
- **RF power control** for the UHF RFID module
- **Tag inventory scanning** and parsing of RFID tag data
- **Event-driven architecture** with an internal event bus
- **MQTT integration** using `paho-mqtt` to publish/subscribe device events
- Simple, extensible design for adding new features or handlers

### Project Structure (Overview)

- `src/main.py` – Application entrypoint, wires up the container, features, and pipeline
- `src/core/` – Core infrastructure: configuration, dependency container, pipeline, worker, state management
- `src/domain/` – Domain models and DTOs for RFID and device data
- `src/events/` – Event definitions and event bus
- `src/externals/` – Integrations (serial client, MQTT client, HTTP client, WebSocket client)
- `src/feature/` – High-level features, including RFID scanner and UHF-specific features

### Requirements

This project uses `pyproject.toml` and `uv` for dependency management.  
You will need:

- Python 3.10+ (recommended)
- `uv` as the Python package/dependency manager
- Access to:
  - A serial port connected to the UHF RFID reader
  - An MQTT broker

### Installation

1. **Clone the repository**

```bash
git clone <your-repo-url>.git
cd UHF_RFID_Hardware-main
```

2. **Install `uv` (if not installed yet)**

Follow the official instructions, for example:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Make sure `uv` is available in your `PATH` (restart your shell if needed).

3. **Create the environment and install dependencies with `uv`**

```bash
uv sync
```

This will create an isolated environment (managed by `uv`) and install all dependencies defined in `pyproject.toml` / `uv.lock`.

### Configuration (.env)

Runtime configuration is loaded from environment variables via `src/core/config.py`.  
Create a `.env` file in the project root (you can base it on `.env.example` if present):

```env
DEVICE_ID=your_device_id

MQTT_BROKER=your_mqtt_broker_host
MQTT_PORT=1883
MQTT_USER=your_mqtt_username
MQTT_PASS=your_mqtt_password
```

Adjust these values to match your environment (device ID, MQTT broker host, port, and credentials).  
Do **not** commit real credentials to version control.

> **Note**: Serial configuration (port, baudrate, etc.) may also be read from config if extended.  
> Make sure your serial port settings in `SerialClient` (and config, if used) match your UHF RFID reader.

### Running the Application

With the `uv` environment prepared and `.env` configured:

```bash
uv run python -m src.main
```

The application will:

- Initialize configuration
- Set up the dependency container
- Open the serial connection to the UHF RFID reader
- Start the RFID pipeline (RF power + tag inventory)
- Connect to the MQTT broker and start handling events

### MQTT Integration

The `MQTTClient` in `src/externals/mqtt_client.py`:

- Connects to the broker defined by `MQTT_BROKER` and `MQTT_PORT`
- Uses `DEVICE_ID` to build a client ID
- Optionally authenticates with `MQTT_USER` and `MQTT_PASS`
- Publishes and subscribes to topics via registered handlers

You can add custom handlers by implementing `MQTTChannelHandler` in `src/externals/mqtt_handlers/` and registering them with the `MQTTClient`.
