# handlers.py
import os
import time
import pyperclip
from tkinter import filedialog, messagebox

from encryption.encryptor import encrypt_image
from encryption.decryptor import decrypt_image
from encryption.key_manager import KeyManager
from utils import show_preview, update_meter_smooth, toggle_password


class EncryptHandler:
    def __init__(self, root):
        self.root = root
        self.key_manager = KeyManager()

    def create_widgets(self, parent, path_var, pass_var, show_var, preview_label, meter, meter_text):
        from ttkbootstrap import ttk

        ttk.Label(parent, text="Select Image File", font=("Segoe UI", 12, "bold")).pack(pady=5)
        entry = ttk.Entry(parent, textvariable=path_var, width=50)
        entry.pack(pady=5)

        ttk.Button(parent, text="📂 Browse", bootstyle="danger-outline",
                   command=lambda: self.select_file(path_var, preview_label)).pack(pady=5)
        ttk.Button(parent, text="❌ Clear", bootstyle="outline-danger",
                   command=lambda: path_var.set('')).pack(pady=2)

        ttk.Label(parent, text="Enter Password", font=("Segoe UI", 12, "bold")).pack(pady=10)
        pass_entry = ttk.Entry(parent, textvariable=pass_var, show="*", width=50)
        pass_entry.pack(pady=5)
        ttk.Checkbutton(parent, text="Show Password", bootstyle="info",
                        variable=show_var, command=lambda: toggle_password(pass_entry, show_var)).pack(pady=2)
        ttk.Button(parent, text="❌ Clear", bootstyle="outline-secondary",
                   command=lambda: pass_var.set('')).pack(pady=2)

        ttk.Button(parent, text="⚡ Encrypt Image", bootstyle="danger",
                   command=lambda: self.encrypt_action(path_var.get(), pass_var.get(), meter, meter_text)).pack(pady=20)

    def select_file(self, path_var, preview_label):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if path:
            path_var.set(path)
            show_preview(path, preview_label)

    def encrypt_action(self, image_path, password, meter, meter_text):
        if not image_path or not password:
            messagebox.showwarning("Missing Input", "Please select an image and enter a password.")
            return
        try:
            key, salt = self.key_manager.generate_key_from_password(password)
            filename = os.path.basename(image_path)
            timestamp = int(time.time())
            output_path = os.path.join('encrypted_images', f"encrypted_{timestamp}_{filename}.enc")
            salt_path = output_path + ".salt"

            update_meter_smooth("Encrypting 🔥", meter, meter_text)

            encrypt_image(image_path, output_path, key, salt)
            with open(salt_path, "wb") as f:
                f.write(salt)

            meter.configure(amountused=100)
            meter_text.config(text="✅ Encryption Complete!")
            pyperclip.copy(output_path)
            messagebox.showinfo("Success", f"Image encrypted!\nSaved as:\n{output_path}\n(Path copied to clipboard)")
        except Exception as e:
            messagebox.showerror("Error", f"Encryption Failed:\n{str(e)}")
        finally:
            meter.configure(amountused=0)
            meter_text.config(text="Status: Idle 💤")


class DecryptHandler:
    def __init__(self, root):
        self.root = root
        self.key_manager = KeyManager()

    def create_widgets(self, parent, path_var, pass_var, show_var, preview_label, meter, meter_text):
        from ttkbootstrap import ttk

        ttk.Label(parent, text="Select Encrypted File", font=("Segoe UI", 12, "bold")).pack(pady=5)
        entry = ttk.Entry(parent, textvariable=path_var, width=50)
        entry.pack(pady=5)

        ttk.Button(parent, text="📂 Browse", bootstyle="info-outline",
                   command=lambda: self.select_file(path_var)).pack(pady=5)
        ttk.Button(parent, text="❌ Clear", bootstyle="outline-danger",
                   command=lambda: path_var.set('')).pack(pady=2)

        ttk.Label(parent, text="Enter Password", font=("Segoe UI", 12, "bold")).pack(pady=10)
        pass_entry = ttk.Entry(parent, textvariable=pass_var, show="*", width=50)
        pass_entry.pack(pady=5)
        ttk.Checkbutton(parent, text="Show Password", bootstyle="info",
                        variable=show_var, command=lambda: toggle_password(pass_entry, show_var)).pack(pady=2)
        ttk.Button(parent, text="❌ Clear", bootstyle="outline-secondary",
                   command=lambda: pass_var.set('')).pack(pady=2)

        ttk.Button(parent, text="🔓 Decrypt Image", bootstyle="info",
                   command=lambda: self.decrypt_action(path_var.get(), pass_var.get(), preview_label, meter, meter_text)).pack(pady=20)

    def select_file(self, path_var):
        path = filedialog.askopenfilename(filetypes=[("Encrypted Files", "*.enc")])
        if path:
            path_var.set(path)

    def decrypt_action(self, enc_path, password, preview_label, meter, meter_text):
        from tkinter import messagebox

        if not enc_path or not password:
            messagebox.showwarning("Missing Input", "Please select a file and enter a password.")
            return
        salt_path = enc_path + ".salt"
        if not os.path.exists(salt_path):
            messagebox.showerror("Error", f"Missing salt file:\n{salt_path}")
            return
        with open(salt_path, "rb") as f:
            salt = f.read()
        try:
            key, _ = self.key_manager.generate_key_from_password(password, salt)
            filename = os.path.basename(enc_path).replace('.enc', '')
            timestamp = int(time.time())
            output_path = os.path.join('decrypted_images', f"decrypted_{timestamp}_{filename}.png')

            update_meter_smooth("Decrypting 🧩", meter, meter_text)
            decrypt_image(enc_path, output_path, password)
            show_preview(output_path, preview_label)

            meter.configure(amountused=100)
            meter_text.config(text="✅ Decryption Complete!")
            pyperclip.copy(output_path)
            messagebox.showinfo("Success", f"Decrypted image saved as:\n{output_path}\n(Path copied to clipboard)")
        except Exception as e:
            messagebox.showerror("Error", f"Decryption Failed:\n{str(e)}")
        finally:
            meter.configure(amountused=0)
            meter_text.config(text="Status: Idle 💤")
