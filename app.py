"""
!/usr/bin/env python
-*- coding: utf-8 -*-

Code that manage all the tkinter window
"""
from download import downloadPlaylist


import tkinter as tk
from tkinter import *
import customtkinter

def chooseFile(entry):
    dossier = customtkinter.filedialog.askdirectory(title="Sélectionnez un dossier")

    if dossier:  # Si l'utilisateur n'annule pas
        entry.delete(0, tk.END)  # Efface le champ texte
        entry.insert(0, dossier) # Met le chemin sélectionné dans le champ

def app():
    root = tk.Tk()
    root.title("MP3 playlist downloader")
    root.state("zoomed")

    url = tk.StringVar()
    tk.Label(text="URL").pack()
    tk.Entry(root, textvariable=url).pack()


    tk.Label(text="Path").pack()
    path = tk.StringVar()
    entry = tk.Entry(root, textvariable=path)
    entryPath = customtkinter.CTkEntry(
        root,
        textvariable=path)
    entry.pack(pady=10)
    buttonPath = customtkinter.CTkButton(
        root, 
        text="Choisir un dossier", 
        corner_radius=50,
        command=lambda: chooseFile(entry)
    )
    buttonPath.pack() 


    btnDownload = customtkinter.CTkButton(
        root,
        text="Download",
        corner_radius=50,
        command=lambda: downloadPlaylist(url=url.get(), path=path.get())
    )
    btnDownload.pack()

    # TODO: afficher les logs d'erreur s'il y en a sans faire crash la fenetre

    tk.Label(root, text="Nothing will work unless you do.").pack()
    tk.Label(root, text="- Maya Angelou").pack()

    root.mainloop()