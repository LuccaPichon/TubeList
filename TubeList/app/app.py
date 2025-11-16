"""
!/usr/bin/env python
-*- coding: utf-8 -*-

Code that manage all the tkinter window
"""
from app.utilsApp import chooseFile
from app.Theme import theme

import tkinter as tk
import customtkinter
from PIL import Image

from download import downloadAny
import threading

class TubeListApp:
    def __init__(self):
        self.root = self._initRoot()

        # Widgets
        self.entryUrl = None
        self.entryPath = None
        self.buttonPath = None
        self.resultDownload = None
        self.progress = None
        self.progressString = None
        self.progressFrame = None

        # UI build
        self._initTitle()
        self._initURL()
        self._initPath()
        self._initDownload()
        self._initLoadbar()
        self._initLoadbarPlaylist()
        self._initLog()
        self._initFooter()

        # Resize behavior
        self.root.bind("<Configure>", self._onResize)


    def _initRoot(self):
        root = tk.Tk()
        root.title("TubeList")
        root.state("zoomed")
        root.geometry("1920x1080")
        root.minsize(480, 480)

        # Icon
        icon = tk.PhotoImage(file='./TubeList/images/icon.png')
        root.iconphoto(True, icon)

        # Colors
        root.configure(background=theme.bgColor)
        root.option_add("*Background", theme.bgColor)
        root.option_add("*Foreground", theme.fgColor)
        root.option_add("*Highlightbackground", theme.highlightBg)

        return root


    def _initTitle(self):
        title = customtkinter.CTkLabel(self.root, text="Welcome to TubeList", font=theme.fontTitle)
        title.pack(anchor="center", pady=(50, 0))

        subtitle = customtkinter.CTkLabel(
            self.root,
            text="The best free and fast converter for Youtube playlist to MP3 format",
            font=theme.fontSubtitle
        )
        subtitle.pack(anchor="center", pady=(10, 50))


    def _initURL(self):
        tk.Label(self.root, text="URL of the playlist / song:", font=theme.fontNormal).pack(anchor="center")

        self.entryUrl = customtkinter.CTkEntry(
            self.root,
            font=theme.fontNormal,
            width=theme.entryWidth + 400,
            placeholder_text="https://www.youtube.com/watch?v=<Your Playlist>",
            placeholder_text_color=theme.placeholderColor
        )
        self.entryUrl.pack(pady=10, ipady=10, anchor="center")
        theme.registeredEntry["entryUrl"] = self.entryUrl


    def _initPath(self):
        tk.Label(self.root, text="Where to download:", font=theme.fontNormal).pack(anchor="center", pady=(20, 0))

        frame = tk.Frame(self.root)
        frame.pack(anchor="center", pady=10)

        self.entryPath = customtkinter.CTkEntry(
            frame,
            font=theme.fontNormal,
            width=theme.entryWidth,
            placeholder_text="C:/Users/<Username>/Documents/",
            placeholder_text_color=theme.placeholderColor
        )
        self.entryPath.pack(padx=10, ipady=10, side="left")
        theme.registeredEntry["entryPath"] = self.entryPath

        folderImg = customtkinter.CTkImage(
            light_image=Image.open('./TubeList/images/folder-icon-size_128.png'),
            dark_image=Image.open('./TubeList/images/folder-icon-size_128.png'),
            size=(32, 32)
        )

        self.buttonPath = customtkinter.CTkButton(
            frame,
            text="Choose a folder",
            font=theme.fontNormal,
            corner_radius=50,
            fg_color=theme.highlightBg,
            image=folderImg,
            command=lambda: chooseFile(self.entryPath)
        )
        self.buttonPath.pack(side="left", ipady=10)

    def _handleDownload(self):
        def run():
            resultString = downloadAny(
                self.entryUrl.get(), 
                self.entryPath.get(), 
                self._progress_callback,
                self._progressPlaylist
            )
            self.resultDownload.set(resultString)

        threading.Thread(target=run, daemon=True).start()

    def _initDownload(self):
        self.resultDownload = tk.StringVar(value="")

        downloadImg = customtkinter.CTkImage(
            light_image=Image.open('./TubeList/images/data-transfer-download-icon-size_64.png'),
            dark_image=Image.open('./TubeList/images/data-transfer-download-icon-size_64.png'),
            size=(32, 32)
        )

        button = customtkinter.CTkButton(
            self.root,
            text="Download",
            corner_radius=50,
            font=theme.fontNormal,
            fg_color=theme.btnDownloadFgColor,
            hover_color=theme.btnDownloadHoverColor,
            image=downloadImg,
            command=self._handleDownload
        )
        button.pack(anchor="center", pady=20, ipadx=15, ipady=15)
        

    def _progress_callback(self, percent):
        self.progress.set(percent)
        self.progressString.set(f"Video: {int(percent * 100)}%")


    def _progressPlaylist(self, index, total):
        percent = index / total
        self.progressPlaylist.set(percent)
        self.progressPlaylistString.set(f"Playlist: {int(percent * 100)}%")

    def _initLoadbar(self):
        self.progressFrame = tk.Frame(self.root, width=theme.loadbarWidth)
        self.progressFrame.pack(anchor="center", pady=10)

        self.progress = customtkinter.CTkProgressBar(self.progressFrame, width=800, progress_color=theme.btnDownloadFgColor)
        self.progress.pack(pady=20, side="right", fill="x")
        self.progress.set(0)
        theme.loadbar = self.progress

        self.progressString = tk.StringVar(value="Video: 0%")
        customtkinter.CTkLabel(self.progressFrame, textvariable=self.progressString, font=theme.fontNormal).pack(side="left", ipadx=15)

    def _initLoadbarPlaylist(self):
        self.progressFramePlaylist = tk.Frame(self.root, width=theme.loadbarWidth)
        self.progressFramePlaylist.pack(anchor="center", pady=10)

        self.progressPlaylist = customtkinter.CTkProgressBar(self.progressFramePlaylist, width=800, progress_color=theme.btnDownloadFgColor)
        self.progressPlaylist.pack(pady=20, side="right", fill="x")
        self.progressPlaylist.set(0)
        theme.loadbarPlaylist = self.progressPlaylist

        self.progressPlaylistString = tk.StringVar(value="Playlist: 0%")
        customtkinter.CTkLabel(self.progressFramePlaylist, textvariable=self.progressPlaylistString, font=theme.fontNormal).pack(side="left", ipadx=15)


    def _initLog(self):
        tk.Label(self.root, textvariable=self.resultDownload, font=theme.fontNormal, wraplength=1500).pack(anchor="center", pady=30)


    def _initFooter(self):
        tk.Label(self.root, text="Nothing will work unless you do.", font=theme.fontNormal).pack(anchor="center")
        tk.Label(self.root, text="- Maya Angelou", font=theme.fontNormal).pack(anchor="center")


    def _onResize(self, event):
        theme.onResize(self.root.winfo_width(), self.buttonPath.winfo_width())


    def run(self):
        self.root.mainloop()
