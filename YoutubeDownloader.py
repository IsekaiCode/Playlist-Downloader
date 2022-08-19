import youtube_dl
import urllib.request

import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys


def find_songs(wd, max_songs: int) -> set:
    # get names of songs from playlist

    t = 0
    songs = set()

    slider = wd.find_element(By.TAG_NAME, 'body')

    names = wd.find_elements(
        By.CLASS_NAME, 'yt-simple-endpoint.style-scope.ytd-playlist-video-renderer')
    for name in names:
        songs.add(name.text)
    while len(songs) < max_songs:
        if t == 10:
            return songs
        t += 1
        slider.send_keys(Keys.END)
        time.sleep(3)
        names = wd.find_elements(
            By.CLASS_NAME, 'yt-simple-endpoint.style-scope.ytd-playlist-video-renderer')
        for name in names:
            songs.add(name.text)

    print(f"number of songs: {len(songs)}")
    return songs


def get_url(name: str) -> str:
    # get url of songs from youtube

    search_keyword = name.replace(" ", "+")
    html = urllib.request.urlopen(
        f"https://www.youtube.com/results?search_query={search_keyword}")
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode('utf-8'))
    new_video = f"https://www.youtube.com/watch?v={video_ids[0]}"
    return new_video


def download(url: str) -> None:
    # download songs from urls

    video_info = youtube_dl.YoutubeDL().extract_info(
        url=url, download=False
    )
    filename = f"{video_info['title']}.mp3"
    options = {
        'format': 'bestaudio/best',
        'keepvideo': False,
        'outtmpl': f"./songs/{filename}",
    }
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']])

    print("Download complete... {}".format(filename))


def main(url: str, max_songs: int, wd_path='./chromedriver.exe'):

    # web driver
    s = Service(wd_path)
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    wd = webdriver.Chrome(service=s, options=options)
    wd.get(url)

    # main
    songs = find_songs(wd, max_songs)
    time.sleep(1)
    wd.close()
    for song in songs:
        try:
            url = get_url(song)
            download(url)
        except:
            print(f"{song} failed to download.")
            continue
