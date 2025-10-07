import re
from pathlib import Path

def read_nfc(file_path):
    text = Path(file_path).read_text(encoding="utf-8", errors="ignore")
    uid_match = re.search(r"UID:\s*([0-9A-Fa-f ]+)", text)
    uid = uid_match.group(1).strip() if uid_match else ""

    data_match = re.search(r"Data\s*Content:\s*((?:[0-9A-Fa-f]{2}\s+)+)", text)
    if not data_match:
        return {"uid": uid, "data_content": ""}
    lines = text.splitlines()
    start = next((i for i, l in enumerate(lines) if "Data Content:" in l), -1)
    collected = lines[start][lines[start].index("Data Content:") + len("Data Content:"):].strip()
    for line in lines[start + 1:]:
        if re.match(r"^[A-Za-z#]", line.strip()):
            break
        collected += " " + line.strip()
    data_content = " ".join(collected.split())
    return {"uid": uid, "data_content": data_content}
