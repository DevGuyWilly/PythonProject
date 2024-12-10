import tkinter as tk
from tkinter import messagebox

# Function to add gratitude entry
def add_entry():
    entry = gratitude_input.get()
    if entry.strip():
        gratitude_list.insert(tk.END, entry)
        gratitude_input.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Please enter something to be thankful for.")

# Function to clear all entries
def clear_entries():
    if messagebox.askyesno("Confirm", "Are you sure you want to clear all entries?"):
        gratitude_list.delete(0, tk.END)

# Create main app window
root = tk.Tk()
root.title("Gratitude Journal")

# Layout
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)

# Widgets
title_label = tk.Label(frame, text="Gratitude Journal", font=("Helvetica", 16, "bold"))
title_label.pack(pady=(0, 10))

gratitude_input = tk.Entry(frame, width=40, font=("Helvetica", 12))
gratitude_input.pack(pady=5)

add_button = tk.Button(frame, text="Add Entry", command=add_entry, width=15, bg="#90EE90", font=("Helvetica", 10))
add_button.pack(pady=5)

gratitude_list = tk.Listbox(frame, width=50, height=15, font=("Helvetica", 12))
gratitude_list.pack(pady=10)

clear_button = tk.Button(frame, text="Clear All", command=clear_entries, width=15, bg="#FFCCCB", font=("Helvetica", 10))
clear_button.pack(pady=5)

# Run the app
root.mainloop()