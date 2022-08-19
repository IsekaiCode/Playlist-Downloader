import tkinter as tk

window = tk.Tk()
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

text2 = tk.Label(window, bg='#856ff8',
                 text="maximum songs :",
                 font=("Helvetica", 14))
text2.place(x=20, y=270)

text2 = tk.Label(window, bg='#856ff8',
                 text="maximum songs :",
                 font=("Helvetica", 14))
text2.place(x=20, y=270)

text3 = tk.Label(window, bg='#856ff8',
                 text="url of the playlist :",
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

max_songs = tk.Text(window, height=1.2, width=10)
max_songs.place(x=240, y=275)

url = tk.Text(window, height=1.2, width=50)
url.place(x=240, y=345)


def on_closing():
    window.destroy()


def clicked():
    if platform.get() == 'youtube':
        from YoutubeDownloader import main
        main(url.get("1.0", 'end-1c'), int(max_songs.get("1.0", 'end-1c')))
    elif platform.get() == 'spotify':
        from SpootifyDownloader import main
        main(url.get("1.0", 'end-1c'), int(max_songs.get("1.0", 'end-1c')))


youtube_button = tk.Button(window, text="submit", width=10, command=clicked)
youtube_button.place(x=345, y=420)

window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
