import customtkinter
import tkinter as tk
from plyer import notification

def chooseFile(entry):
    file = customtkinter.filedialog.askdirectory(title="Sélectionnez un dossier")

    if file:
        entry.delete(0, tk.END)
        entry.insert(0, file)

def notificationDownloadEnd():
    notification.notify(
        title = "TubeList",
        message = "Your video is downloaded",
        ticker = "TubeList",
        app_icon = "./TubeList/images/icon.ico",
        timeout = 10,
        toast = True
    )