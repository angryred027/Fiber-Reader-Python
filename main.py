import json
import string
from read_nfc import read_nfc

def hex_to_ascii(hex_string):
    try:
        ascii_text = bytes.fromhex(hex_string).decode('ascii', errors='ignore')
        printable = ''.join(ch for ch in ascii_text if ch in string.printable)
        return printable.strip()
    except Exception:
        return ""

def check_part_number(ascii_text, uid):
    approved_parts = {
        "AXR-1023": "E0 04 01 08 46 58 0F C8",  # Example UID
        "BGT-5500": "E0 04 01 08 12 34 56 78",
        "ZTR-9999": "E0 04 01 08 11 22 33 44"
    }
    for part, approved_uid in approved_parts.items():
        if part in ascii_text and uid == approved_uid:
            return {"status": "match", "part_number": part, "uid": uid}
    return {"status": "no_match", "uid": uid, "ascii_text": ascii_text}

if __name__ == "__main__":
    file_path = "Green.nfc"
    nfc_data = read_nfc(file_path)
    uid = nfc_data["uid"]
    hex_data = nfc_data["data_content"]

    ascii_text = hex_to_ascii(hex_data)
    print("UID:", uid)
    print("Total bytes:", len(hex_data.split()))
    print("ASCII preview:", ascii_text)
    
    result = check_part_number(ascii_text, uid)
    print("Result JSON:", json.dumps(result, indent=2))