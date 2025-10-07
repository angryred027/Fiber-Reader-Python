import json

def check_part_number(hex_string):
    try:
        ascii_text = bytes.fromhex(hex_string).decode('ascii')
    except ValueError:
        return json.dumps({"status": "error", "message": "Invalid hex input"})

    approved_parts = [
        "AXR-1023",
        "BGT-5500",
        "ZTR-9999",
        "TX-11A",
        "TEST123"
    ]

    if ascii_text in approved_parts:
        result = {"status": "match", "part_number": ascii_text}
    else:
        result = {"status": "no_match", "input_text": ascii_text}

    return json.dumps(result)


if __name__ == "__main__":
    example_hex = "54582d313141"
    response = check_part_number(example_hex)
    print(response)