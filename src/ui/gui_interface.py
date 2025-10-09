import os
import time
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import Meter
from tkinter import filedialog, messagebox, PhotoImage
import pyperclip

from encryption.encryptor import encrypt_image
from encryption.decryptor import decrypt_image
from encryption.key_manager import KeyManager


def start_gui():
    """🔥 Image Encryption GUI with Drag&Drop, Preview, Clear Buttons & Show Password 🔥"""

    # --- Create folders ---
    os.makedirs('encrypted_images', exist_ok=True)
    os.makedirs('decrypted_images', exist_ok=True)

    # --- Main Window ---
    app = ttk.Window(
        title="🖼️ Image Encryption System - Secure & Smart",
        themename="cyborg",
        size=(1100, 650)
    )
    app.place_window_center()

    key_manager_instance = KeyManager()

    # --- UI Variables ---
    encrypt_path_var = ttk.StringVar()
    decrypt_path_var = ttk.StringVar()
    encrypt_pass_var = ttk.StringVar()
    decrypt_pass_var = ttk.StringVar()
    current_theme = ttk.StringVar(value="cyborg")
    show_encrypt_pass_var = ttk.BooleanVar(value=False)
    show_decrypt_pass_var = ttk.BooleanVar(value=False)

    # --- HEADER ---
    ttk.Label(
        app,
        text="🔐 Image Encryption System",
        font=("Segoe UI", 28, "bold"),
        foreground="#FF073A"
    ).pack(pady=25)

    # --- TOP BUTTON FRAME ---
    top_button_frame = ttk.Frame(app)
    top_button_frame.pack(pady=10)

    def toggle_theme():
        new_theme = "flatly" if current_theme.get() == "cyborg" else "cyborg"
        app.style.theme_use(new_theme)
        current_theme.set(new_theme)
        meter.bootstyle = "success" if new_theme == "flatly" else "danger"
        meter.configure(bootstyle=meter.bootstyle)

    ttk.Button(
        top_button_frame,
        text="🌗 Toggle Dark/Light Mode",
        bootstyle="outline-info",
        command=toggle_theme
    ).pack()

    # --- MAIN FRAME ---
    main_frame = ttk.Frame(app)
    main_frame.pack(fill=BOTH, expand=True, padx=25, pady=10)
    card_opts = dict(padding=20, relief=RAISED, borderwidth=3, bootstyle="dark")

    # --- ENCRYPTION FRAME ---
    encrypt_frame = ttk.Labelframe(main_frame, text="Encrypt Section", **card_opts)
    encrypt_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=20, pady=10)

    ttk.Label(encrypt_frame, text="Select Image File", font=("Segoe UI", 12, "bold")).pack(pady=5)
    encrypt_entry = ttk.Entry(encrypt_frame, textvariable=encrypt_path_var, width=50)
    encrypt_entry.pack(pady=5)
    ttk.Button(encrypt_frame, text="📂 Browse", bootstyle="danger-outline",
               command=lambda: select_encrypt_file()).pack(pady=5)
    ttk.Button(encrypt_frame, text="❌ Clear", bootstyle="outline-danger",
               command=lambda: encrypt_path_var.set('')).pack(pady=2)

    ttk.Label(encrypt_frame, text="Enter Password", font=("Segoe UI", 12, "bold")).pack(pady=10)
    encrypt_pass_entry = ttk.Entry(encrypt_frame, textvariable=encrypt_pass_var, show="*", width=50)
    encrypt_pass_entry.pack(pady=5)
    ttk.Checkbutton(encrypt_frame, text="Show Password", bootstyle="info",
                    variable=show_encrypt_pass_var,
                    command=lambda: toggle_password(encrypt_pass_entry, show_encrypt_pass_var)).pack(pady=2)
    ttk.Button(encrypt_frame, text="❌ Clear", bootstyle="outline-secondary",
               command=lambda: encrypt_pass_var.set('')).pack(pady=2)

    ttk.Button(encrypt_frame, text="⚡ Encrypt Image", bootstyle="danger",
               command=lambda: encrypt_action()).pack(pady=20)

    encrypt_preview_label = ttk.Label(encrypt_frame)
    encrypt_preview_label.pack(pady=5)

    # --- DECRYPTION FRAME ---
    decrypt_frame = ttk.Labelframe(main_frame, text="Decrypt Section", **card_opts)
    decrypt_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=20, pady=10)

    ttk.Label(decrypt_frame, text="Select Encrypted File", font=("Segoe UI", 12, "bold")).pack(pady=5)
    decrypt_entry = ttk.Entry(decrypt_frame, textvariable=decrypt_path_var, width=50)
    decrypt_entry.pack(pady=5)
    ttk.Button(decrypt_frame, text="📂 Browse", bootstyle="info-outline",
               command=lambda: select_decrypt_file()).pack(pady=5)
    ttk.Button(decrypt_frame, text="❌ Clear", bootstyle="outline-danger",
               command=lambda: decrypt_path_var.set('')).pack(pady=2)

    ttk.Label(decrypt_frame, text="Enter Password", font=("Segoe UI", 12, "bold")).pack(pady=10)
    decrypt_pass_entry = ttk.Entry(decrypt_frame, textvariable=decrypt_pass_var, show="*", width=50)
    decrypt_pass_entry.pack(pady=5)
    ttk.Checkbutton(decrypt_frame, text="Show Password", bootstyle="info",
                    variable=show_decrypt_pass_var,
                    command=lambda: toggle_password(decrypt_pass_entry, show_decrypt_pass_var)).pack(pady=2)
    ttk.Button(decrypt_frame, text="❌ Clear", bootstyle="outline-secondary",
               command=lambda: decrypt_pass_var.set('')).pack(pady=2)

    ttk.Button(decrypt_frame, text="🔓 Decrypt Image", bootstyle="info",
               command=lambda: decrypt_action()).pack(pady=20)

    decrypt_preview_label = ttk.Label(decrypt_frame)
    decrypt_preview_label.pack(pady=5)

    # --- PROGRESS METER ---
    meter_frame = ttk.Frame(app)
    meter_frame.pack(pady=20)
    meter = Meter(
        meter_frame, bootstyle="danger", subtext="Progress",
        amounttotal=100, metersize=170, stripethickness=8,
        interactive=False, textfont=("Segoe UI", 14, "bold")
    )
    meter.pack(pady=10)
    meter_text = ttk.Label(app, text="Status: Idle 💤", font=("Segoe UI", 12))
    meter_text.pack()

    # --- HELPER FUNCTIONS ---
    def update_meter_smooth(task_name):
        for i in range(101):
            meter.configure(amountused=i)
            meter_text.config(text=f"{task_name}... {i}%")
            app.update()
            time.sleep(0.01)

    def toggle_password(entry, var):
        entry.configure(show="" if var.get() else "*")

    def show_preview(path, label):
        try:
            img = PhotoImage(file=path)
            img = img.subsample(max(img.width() // 150, 1), max(img.height() // 150, 1))
            label.configure(image=img)
            label.image = img
        except:
            label.configure(image='')

    def select_encrypt_file():
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if path:
            encrypt_path_var.set(path)
            show_preview(path, encrypt_preview_label)

    def select_decrypt_file():
        path = filedialog.askopenfilename(filetypes=[("Encrypted Files", "*.enc")])
        if path:
            decrypt_path_var.set(path)

    def encrypt_action():
        image_path = encrypt_path_var.get()
        password = encrypt_pass_var.get()
        if not image_path or not password:
            messagebox.showwarning("Missing Input", "Please select an image and enter a password.")
            return
        try:
            key, salt = key_manager_instance.generate_key_from_password(password)
            filename = os.path.basename(image_path)
            timestamp = int(time.time())
            output_path = os.path.join('encrypted_images', f"encrypted_{timestamp}_{filename}.enc")
            salt_path = output_path + ".salt"

            update_meter_smooth("Encrypting 🔥")

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

    def decrypt_action():
        enc_path = decrypt_path_var.get()
        password = decrypt_pass_var.get()
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
            key, _ = key_manager_instance.generate_key_from_password(password, salt)
            filename = os.path.basename(enc_path).replace('.enc', '')
            timestamp = int(time.time())
            output_path = os.path.join('decrypted_images', f"decrypted_{timestamp}_{filename}.png")

            update_meter_smooth("Decrypting 🧩")

            decrypt_image(enc_path, output_path, password)
            show_preview(output_path, decrypt_preview_label)

            meter.configure(amountused=100)
            meter_text.config(text="✅ Decryption Complete!")
            pyperclip.copy(output_path)
            messagebox.showinfo("Success", f"Decrypted image saved as:\n{output_path}\n(Path copied to clipboard)")

        except Exception as e:
            messagebox.showerror("Error", f"Decryption Failed:\n{str(e)}")
        finally:
            meter.configure(amountused=0)
            meter_text.config(text="Status: Idle 💤")

    # --- FOOTER ---
    ttk.Label(
        app,
        text="Developed by ASH | Secure AES-based Encryption",
        font=("Segoe UI", 11, "italic"),
        foreground="#FF073A"
    ).pack(pady=15)

    app.mainloop()
