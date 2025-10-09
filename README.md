# 🖼️ Image Encryption GUI - Secure & Smart

A modern GUI application to **encrypt and decrypt images** with AES-based encryption. Built with **Python**, **ttkbootstrap**, and **Tkinter**.

---

## Features

- 🔐 AES-based image encryption & decryption
- 🌗 Dark/Light theme toggle
- ⚡ Progress meter with smooth updates
- 🖼️ Image preview before encryption/decryption
- 📂 Browse or drag & drop support (future enhancement)
- 🔑 Password input with show/hide option
- 📋 Clipboard copy of output file path
- ✅ Error handling and status messages

---

## File Structure

image_encryption_gui/
│
├── gui.py # Main GUI layout
├── handlers.py # Encrypt/Decrypt logic
├── utils.py # Helper functions
├── encryption/ # AES logic modules
│ ├── encryptor.py
│ ├── decryptor.py
│ └── key_manager.py
├── encrypted_images/ # Auto-created output folder
├── decrypted_images/ # Auto-created output folder
├── requirements.txt # Python dependencies
└── README.md
