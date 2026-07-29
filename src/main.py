from bootstrap.app import build_app


def main() -> None:

    app = build_app()

    app.serial.connect()
    app.mqtt.connect()

    try:
        app.scheduler.run()
    except KeyboardInterrupt:   
        pass
    finally:
        app.mqtt.disconnect()
        app.serial.disconnect()


if __name__ == "__main__":
    main()