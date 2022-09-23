import tkinter as tk
from threading import Thread

import spotifydownloader as sd
import ytdownloader as yd

window = tk.Tk()
window.title("Playlist Downloader")

window.geometry(
    f"800x500+{(window.winfo_screenwidth()//2)-400}+{(window.winfo_screenheight()//2)-300}")
window.configure(bg='#856ff8')

title = tk.Label(window, bg='#856ff8',
                 text="Playlist Downloader For Youtube and Spotify",
                 font=("Helvetica", 23))
title.place(x=20, y=40)

text1 = tk.Label(window, bg='#856ff8',
                 text="type of playlist :",
                 font=("Helvetica", 15))
text1.place(x=20, y=200)

text3 = tk.Label(window, bg='#856ff8',
                 text="playlist_url of the playlist :",
                 font=("Helvetica", 14))
text3.place(x=20, y=340)

warning = tk.Label(window, bg='#856ff8',
                   text="update your chromedriver to the latest version !!",
                   font=("Helvetica", 10),
                   foreground="#eed202")
warning.place(x=20, y=470)

platform = tk.StringVar(window)
platform.set("youtube")

options = tk.OptionMenu(window, platform, "youtube", "spotify")
options.place(x=240, y=202)

playlist_url = tk.Text(window, height=1.2, width=50)
playlist_url.place(x=240, y=345)


def on_closing():
    window.destroy()


def threading():
        # Call work function
        t1 = Thread(target=clicked)
        t1.start()

def clicked():
    if platform.get() == 'youtube':
        yt_url = playlist_url.get("1.0", 'end-1c')
        yd.main(yt_url)
    elif platform.get() == 'spotify':
        sp_url = playlist_url.get("1.0", 'end-1c')
        sd.main(sp_url)


button = tk.Button(window, text="submit", width=10, command=threading)
button.place(x=345, y=420)

window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
