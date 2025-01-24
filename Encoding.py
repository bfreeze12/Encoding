#Group Member:
#1211100640 NICHOLES TEY YEE KEE
#1221303466 SIM KIM SENG
#1211102360 CHONG DING ZHE

import heapq
from collections import Counter
from math import log2
import pandas as pd
import tkinter as tk
from tkinter import messagebox, scrolledtext
import datetime

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree_with_stages(frequencies):
    heap = [HuffmanNode(char, freq) for char, freq in frequencies.items()]
    heapq.heapify(heap)
    stages = []

    while len(heap) > 1:
        heap.sort(key=lambda node: node.freq)
        current_stage = [(node.char if node.char else '-', node.freq) for node in heap]
        stages.append(current_stage)

        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    if heap:
        final_stage = [(node.char if node.char else '-', node.freq) for node in heap]
        stages.append(final_stage)

    return heap[0] if heap else None, stages

def generate_encoding_table(root):
    encoding_table = {}

    def encode(node, current_code):
        if node is None:
            return
        if node.char is not None:
            encoding_table[node.char] = current_code
        encode(node.left, current_code + "0")
        encode(node.right, current_code + "1")

    encode(root, "")
    return encoding_table

def calculate_efficiency(frequencies, encoding_table):
    total_symbols = sum(frequencies.values())
    probabilities = {char: freq / total_symbols for char, freq in frequencies.items()}

    entropy = -sum(p * log2(p) for p in probabilities.values() if p > 0)
    avg_length = sum(len(encoding_table[char]) * probabilities[char] for char in frequencies)
    efficiency = (entropy / avg_length) * 100 if avg_length > 0 else 0

    return entropy, avg_length, efficiency

def display_stages_table(stages):
    max_length = max(len(stage) for stage in stages)
    normalized_stages = [stage + [(None, None)] * (max_length - len(stage)) for stage in stages]
    stage_dict = {f"Stage {i+1}": [f"{char} ({freq})" if char is not None else "" for char, freq in stage] for i, stage in enumerate(normalized_stages)}
    df_stages = pd.DataFrame(stage_dict)
    return df_stages

def display_encoding_table_pandas(encoding_table, frequencies):
    rows = []
    for char, freq in frequencies.items():
        codeword = encoding_table.get(char, "")
        code_length = len(codeword)
        rows.append([char, freq, codeword, code_length])
    encoding_df = pd.DataFrame(rows, columns=["Symbol", "Frequency", "Codeword", "Codeword Length"])
    return encoding_df

def perform_huffman_encoding():
    try:
        name = entry_name.get().strip().upper()

        vowels = [char for char in name if char in "AEIOU"]
        if len(vowels) < 2:
            messagebox.showerror("Input Error", "The name must contain at least two vowels.")
            return

        text = "AERIOUS" + vowels[0] + vowels[1]

        frequencies = Counter(text)

        root, stages = build_huffman_tree_with_stages(frequencies)

        encoding_table = generate_encoding_table(root)

        entropy, avg_length, efficiency = calculate_efficiency(frequencies, encoding_table)

        display_huffman_stages(stages)

        encoding_df = display_encoding_table_pandas(encoding_table, frequencies)
        display_encoding_table_pandas_gui(encoding_df)

        display_efficiency(entropy, avg_length, efficiency)

    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")

def display_huffman_stages(stages):
    try:
        df_stages = display_stages_table(stages)
        txt_stages.config(state='normal')
        txt_stages.delete('1.0', tk.END)
        txt_stages.insert(tk.END, "Stages of Huffman Tree Construction:\n")
        txt_stages.insert(tk.END, df_stages.to_string(index=False))
        txt_stages.config(state='disabled')  # Disable editing
    except Exception as e:
        messagebox.showerror("Error", f"Failed to display Huffman stages:\n{e}")

def display_encoding_table_pandas_gui(encoding_df):
    try:
        txt_encoding_table.config(state='normal')
        txt_encoding_table.delete('1.0', tk.END)
        txt_encoding_table.insert(tk.END, "Huffman Encoding Table:\n")
        txt_encoding_table.insert(tk.END, encoding_df.to_string(index=False))
        txt_encoding_table.config(state='disabled')
    except Exception as e:
        messagebox.showerror("Error", f"Failed to display encoding table:\n{e}")

def display_efficiency(entropy, avg_length, efficiency):
    try:
        txt_efficiency.config(state='normal')
        txt_efficiency.delete('1.0', tk.END)
        txt_efficiency.insert(tk.END, "Efficiency Calculations:\n")
        txt_efficiency.insert(tk.END, f"Entropy: {entropy:.4f} bits/symbol\n")
        txt_efficiency.insert(tk.END, f"Average Code Length: {avg_length:.4f} bits/symbol\n")
        txt_efficiency.insert(tk.END, f"Efficiency: {efficiency:.2f}%\n")
        txt_efficiency.config(state='disabled')
    except Exception as e:
        messagebox.showerror("Error", f"Failed to display efficiency calculations:\n{e}")

def save_results():
    try:
        name = entry_name.get().strip().upper()
        if not name:
            messagebox.showerror("Save Error", "No data to save. Please perform encoding first.")
            return

        encoding_table_text = txt_encoding_table.get('1.0', tk.END).strip()
        efficiency_text = txt_efficiency.get('1.0', tk.END).strip()
        stages_text = txt_stages.get('1.0', tk.END).strip()

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"huffman_results_{timestamp}.txt"

        with open(filename, "w") as file:
            file.write(f"Group Member's Name: {name}\n")
            file.write(f"Constructed Text: {'AERIOUS' + ''.join([char for char in name if char in 'AEIOU'][:2])}\n\n")
            file.write(f"{stages_text}\n\n")
            file.write(f"{encoding_table_text}\n\n")
            file.write(f"{efficiency_text}\n")

        messagebox.showinfo("Save Successful", f"Results have been saved to {filename}")

    except Exception as e:
        messagebox.showerror("Save Error", f"Failed to save results:\n{e}")

def clear_all():
    entry_name.delete(0, tk.END)
    txt_stages.config(state='normal')
    txt_stages.delete('1.0', tk.END)
    txt_stages.config(state='disabled')

    txt_encoding_table.config(state='normal')
    txt_encoding_table.delete('1.0', tk.END)
    txt_encoding_table.config(state='disabled')

    txt_efficiency.config(state='normal')
    txt_efficiency.delete('1.0', tk.END)
    txt_efficiency.config(state='disabled')

window = tk.Tk()
window.title("Advanced Huffman Encoding Tool")
window.geometry("900x800")

label_name = tk.Label(window, text="Enter a group member's name:", font=("Arial", 12))
label_name.pack(pady=10)

entry_name = tk.Entry(window, width=50, font=("Arial", 12))
entry_name.pack(pady=5)

btn_generate = tk.Button(window, text="Generate Encoding", command=perform_huffman_encoding, font=("Arial", 12))
btn_generate.pack(pady=10)

btn_save = tk.Button(window, text="Save Results", command=save_results, font=("Arial", 12))
btn_save.pack(pady=5)

btn_clear = tk.Button(window, text="Clear All", command=clear_all, font=("Arial", 12))
btn_clear.pack(pady=5)

separator = tk.Frame(window, height=2, bd=1, relief=tk.SUNKEN)
separator.pack(fill=tk.X, padx=5, pady=10)

label_stages = tk.Label(window, text="Stages of Huffman Tree Construction:", font=("Arial", 12))
label_stages.pack(pady=5)

txt_stages = scrolledtext.ScrolledText(window, width=100, height=10, wrap=tk.WORD, state='disabled', font=("Courier New", 10))
txt_stages.pack(pady=5)

label_encoding = tk.Label(window, text="Huffman Encoding Table:", font=("Arial", 12))
label_encoding.pack(pady=5)

txt_encoding_table = scrolledtext.ScrolledText(window, width=100, height=15, wrap=tk.WORD, state='disabled', font=("Courier New", 10))
txt_encoding_table.pack(pady=5)

label_efficiency = tk.Label(window, text="Efficiency Calculations:", font=("Arial", 12))
label_efficiency.pack(pady=5)

txt_efficiency = scrolledtext.ScrolledText(window, width=100, height=7, wrap=tk.WORD, state='disabled', font=("Courier New", 10))
txt_efficiency.pack(pady=5)

window.mainloop()
