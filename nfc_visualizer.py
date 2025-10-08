import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import re

# -------------------------------------------------
# Utility: Parse hex string into list of 4-byte blocks
# -------------------------------------------------
def parse_hex_blocks(hex_data, block_size=4):
    hex_bytes = re.findall(r"[0-9A-Fa-f]{2}", hex_data)
    blocks = [hex_bytes[i:i + block_size] for i in range(0, len(hex_bytes), block_size)]
    return blocks


# -------------------------------------------------
# Utility: Check if a block is printable ASCII
# -------------------------------------------------
def is_printable_block(block):
    try:
        s = bytes(int(b, 16) for b in block).decode("ascii")
        return all(32 <= ord(c) <= 126 for c in s)
    except Exception:
        return False


# -------------------------------------------------
# Visualize parsed blocks in the scrollable UI
# -------------------------------------------------
def visualize(hex_data):
    # Clear previous content
    for widget in frame.winfo_children():
        widget.destroy()

    blocks = parse_hex_blocks(hex_data)
    for i, block in enumerate(blocks):
        hex_str = " ".join(block)
        try:
            ascii_str = bytes(int(b, 16) for b in block).decode("ascii", errors="ignore")
            ascii_str = ''.join(c if 32 <= ord(c) <= 126 else '.' for c in ascii_str)
        except:
            ascii_str = "----"

        color = "lightgreen" if is_printable_block(block) else "lightcoral"

        label = tk.Label(
            frame,
            text=f"Block {i:03}:  {hex_str:<15} | {ascii_str}",
            bg=color,
            anchor="w",
            font=("Consolas", 10),
            padx=5
        )
        label.pack(fill="x", padx=2, pady=1)


# -------------------------------------------------
# File selection and parsing logic
# -------------------------------------------------
def open_file():
    path = filedialog.askopenfilename(
        title="Select NFC file",
        filetypes=[("NFC files", "*.nfc"), ("Text files", "*.txt"), ("All files", "*.*")]
    )
    if not path:
        return

    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read file:\n{e}")
        return

    match = re.search(r"Data Content:\s*(.+?)(?:#|$)", text, re.DOTALL)
    if not match:
        messagebox.showwarning("Not Found", "No 'Data Content' section found in file.")
        return

    hex_data = match.group(1).strip()
    visualize(hex_data)


# -------------------------------------------------
# Build main Tkinter window
# -------------------------------------------------
root = tk.Tk()
root.title("Flipper NFC Block Visualizer")
root.geometry("700x600")

title_label = tk.Label(root, text="NFC Data Content Visualizer", font=("Segoe UI", 12, "bold"))
title_label.pack(pady=8)

open_btn = tk.Button(root, text="Open .nfc File", command=open_file, bg="#4CAF50", fg="white", padx=10, pady=5)
open_btn.pack(pady=5)

# Scrolled container
scroll_canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=scroll_canvas.yview)
scroll_frame = tk.Frame(scroll_canvas)

scroll_frame.bind(
    "<Configure>",
    lambda e: scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))
)

scroll_canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
scroll_canvas.configure(yscrollcommand=scrollbar.set)

scroll_canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

frame = scroll_frame  # alias for visualization target

# Run UI
root.mainloop()
