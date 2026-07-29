class UHFRFIDParser():

    def inventory(self, data: bytes) -> list[str]:
        tags: list[str] = []
        offset = 0

        while offset < len(data):
            frame_length = data[offset]
            frame = data[offset:offset + frame_length + 1]

            if len(frame) < 7:
                break

            if frame[2] == 0x01:
                epc_length = frame[6]

                if epc_length > 0 and 7 + epc_length <= len(frame):
                    epc = frame[7:7 + epc_length]
                    tags.append(epc.hex().upper())

            offset += frame_length + 1

        return tags