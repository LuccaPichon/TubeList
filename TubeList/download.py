#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Code to download audio

from pytubefix import Playlist, YouTube
from pytubefix.exceptions import RegexMatchError, BotDetection
import os

def _downloadAudio(obj, path: str):
    stream = obj.streams.get_audio_only()
    stream.download(output_path=path)

def _on_progress(stream, chunk: bytes, bytes_remaining: int, progress_callback):
    filesize = stream.filesize
    bytes_received = filesize - bytes_remaining
    percent = bytes_received / filesize

    if progress_callback:
        progress_callback(percent=percent)

def _downloadVideo(url: str, path: str, progress_callback):
    yt = YouTube(
        url, 
        'WEB', 
        on_progress_callback = lambda stream, chunk, bytes_remaining: _on_progress(stream, chunk, bytes_remaining, progress_callback))

    print(yt.title)
    _downloadAudio(yt, path)

    return yt.title

def _downloadPlaylist(url: str, path: str):
    pl = Playlist(url)
    listTitle = []

    for video in pl.videos:
        print(video.title)
        _downloadAudio(video, path)
        listTitle.append(video.title)

    return listTitle

def _checkPath(path: str):
    if path == "":
        path = "./"
        return False

    if os.path.isdir(path):
        return False
    
    return True

def downloadAny(url: str, path: str, progress_callback):
    if url == None or path == None or progress_callback == None:
        print(f"Missing argument {url}, {path}, {progress_callback}")
        return f"Missing argument {url}, {path}, {progress_callback}"

    path = path.strip()
    url = url.strip()
    title = ""

    if _checkPath(path):
        return "Path is not valid"

    try: 
        title = _downloadVideo(url, path, progress_callback)
        return f"Downloaded : {title}"
    except RegexMatchError:
        try:
            title = _downloadPlaylist(url, path)
            return f"Downloaded : {title} "
        except (RegexMatchError, KeyError) as e:
            return f"404: Url is not a valid youtube url\n\n{e}"
        except BotDetection as e:
            return f"403: This request was detected as a bot (too much request).\nYou should use another wifi to download\n\n{e}"
        except Exception as e:
            print("downloadPlaylist: ", e)
            return e
    except BotDetection as e:
        return f"403: This request was detected as a bot (too much request).\nYou should use another wifi to download\n\n{e}"
    except Exception as e:
        print("Error downloadVideo: ", e)
        return e