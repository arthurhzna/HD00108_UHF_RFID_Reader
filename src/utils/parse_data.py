def parse_data_tag_inventory(data: bytes) -> list[str]:
    i = 0
    tags = []

    while i < len(data):
        length = data[i]
        frame = data[i:i + length + 1]

        if len(frame) < 7:
            break

        if frame[2] == 0x01:  # inventory response
            epc_len = frame[6]

            if epc_len > 0 and 7 + epc_len <= len(frame):
                epc = frame[7:7 + epc_len]
                tags.append(epc.hex().upper())

        i += length + 1

    return tags