# Image Encryption GUI - Secure & Smart

A modern GUI application to **encrypt and decrypt images** with AES-based encryption. Built with **Python**, **ttkbootstrap**, and **Tkinter**.

---

## Features

-  AES-based image encryption & decryption
-  Dark/Light theme toggle
-  Progress meter with smooth updates
-  Image preview before encryption/decryption
-  Browse or drag & drop support (future enhancement)
-  Password input with show/hide option
-  Clipboard copy of output file path
-  Error handling and status messages

---

## File structure

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

## Output:
Main page:
<img width="1897" height="958" alt="Screenshot 2025-10-22 111856" src="https://github.com/user-attachments/assets/65e89a94-7536-4c31-a066-52a7c9aef80b" />
<img width="1898" height="960" alt="Screenshot 2025-10-22 111909" src="https://github.com/user-attachments/assets/4002b285-1900-496f-a3bc-5f34e6d26f70" />
Encryption of image:
<img width="943" height="568" alt="Screenshot 2025-10-22 112056" src="https://github.com/user-attachments/assets/7fc24112-285a-42d8-9fc1-78186778a8c0" />
<img width="1885" height="894" alt="Screenshot 2025-10-22 112112" src="https://github.com/user-attachments/assets/078b76f7-e149-4430-9d1f-38cdc75f2832" />
Decryption of image:
Encrypted image save as a .enc file in a encrypted images folder and we can select it and give a correct password to decrypt
<img width="966" height="629" alt="Screenshot 2025-10-22 112147" src="https://github.com/user-attachments/assets/cbd2034d-a651-4628-a830-f3815ab32f57" />
<img width="1895" height="957" alt="Screenshot 2025-10-22 112215" src="https://github.com/user-attachments/assets/45194102-2b2f-4763-af10-762dc2f460ce" />




