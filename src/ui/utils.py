# utils.py
import time
from tkinter import PhotoImage


def show_preview(path, label):
    """Show image preview in label"""
    try:
        img = PhotoImage(file=path)
        img = img.subsample(max(img.width() // 150, 1), max(img.height() // 150, 1))
        label.configure(image=img)
        label.image = img
    except:
        label.configure(image='')


def toggle_password(entry, var):
    """Show or hide password"""
    entry.configure(show="" if var.get() else "*")


def update_meter_smooth(task_name, meter, meter_text):
    """Animate the progress meter"""
    for i in range(101):
        meter.configure(amountused=i)
        meter_text.config(text=f"{task_name}... {i}%")
        meter_text.update()
        time.sleep(0.01)
