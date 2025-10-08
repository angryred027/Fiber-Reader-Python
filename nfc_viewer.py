import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import re

def normalize_hex(s):
    s = re.sub(r'#.*', '', s)
    s = re.sub(r'[^0-9A-Fa-f]+', ' ', s).strip()
    return s

def hex_to_bytes(hex_str):
    hex_str = normalize_hex(hex_str)
    if not hex_str:
        return b''
    hex_str = re.sub(r'\s+', '', hex_str)
    return bytes.fromhex(hex_str)

def printable_ascii(b):
    return ''.join(chr(x) if 32 <= x <= 126 else '.' for x in b)

def try_bcd(b):
    digits = []
    for byte in b:
        hi, lo = (byte >> 4) & 0xF, byte & 0xF
        if hi > 9 or lo > 9:
            return ''
        digits.append(str(hi))
        digits.append(str(lo))
    return ''.join(digits).lstrip('0') or '0'

def scan_refs(ascii_text):
    patterns = re.findall(r'\b\d{3,}-\d+\b', ascii_text)
    return list(dict.fromkeys(patterns))

class NFCViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Flipper NFC Data Viewer")
        self.geometry("900x600")

        self.create_widgets()
        self.data = b''

    def create_widgets(self):
        frame = tk.Frame(self)
        frame.pack(fill="x", pady=5)

        tk.Button(frame, text="Load File", command=self.load_file).pack(side="left", padx=5)
        tk.Button(frame, text="Detect REF Patterns", command=self.detect_refs).pack(side="left", padx=5)

        self.ref_label = tk.Label(frame, text="Detected REF: None", fg="blue")
        self.ref_label.pack(side="left", padx=10)

        # Table
        cols = ("Block", "Hex", "ASCII", "BCD")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=180 if c != "Block" else 60, anchor="center")
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(fill="both", expand=True, side="left")
        vsb.pack(fill="y", side="right")

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt *.nfc"), ("All files", "*.*")])
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file:\n{e}")
            return

        # Extract "Data Content:" section if exists
        match = re.search(r"Data Content:\s*([0-9A-Fa-f\s]+)", content)
        hex_data = match.group(1) if match else content
        self.data = hex_to_bytes(hex_data)
        self.populate_table()

    def populate_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        if not self.data:
            return

        block_size = 4
        blocks = [self.data[i:i+block_size] for i in range(0, len(self.data), block_size)]

        for idx, b in enumerate(blocks):
            hex_str = ' '.join(f"{x:02X}" for x in b)
            ascii_str = printable_ascii(b)
            bcd_str = try_bcd(b)
            self.tree.insert("", "end", values=(idx, hex_str, ascii_str, bcd_str))

        self.ref_label.config(text="Detected REF: None")

    def detect_refs(self):
        if not self.data:
            messagebox.showinfo("No data", "Load an NFC file first.")
            return
        ascii_stream = ''.join(chr(x) if 32 <= x <= 126 else ' ' for x in self.data)
        refs = scan_refs(ascii_stream)
        if refs:
            self.ref_label.config(text=f"Detected REF: {', '.join(refs)}", fg="green")
        else:
            self.ref_label.config(text="Detected REF: None", fg="red")

if __name__ == "__main__":
    app = NFCViewer()
    app.mainloop()
