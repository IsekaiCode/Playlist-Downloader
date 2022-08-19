import youtube_dl
import urllib.request

import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains


def get_songs(wd, max_songs: int) -> set:
    # get all songs from spootify playlist using selenium

    class_name = "gvLrgQXBFVW6m9MscfFA"
    slider = wd.find_element(
        By.XPATH, '//*[@id="main"]/div/div[2]/div[3]/div[1]/div[2]/div[4]/div/div')

    t = 0
    songs = set()
    action = ActionChains(wd)

    while len(songs) < max_songs:
        if t == 20:
            return songs
        t += 1
        action.drag_and_drop_by_offset(slider, 0, 50)
        action.perform()
        time.sleep(1)
        names = wd.find_elements(By.CLASS_NAME, class_name)
        for name in names:
            songs.add(name.text.replace('\n', ' '))

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

    # Web driver
    s = Service(wd_path)
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    wd = webdriver.Chrome(service=s, options=options)
    wd.get(url)

    # Run
    songs = get_songs(wd, max_songs)
    time.sleep(1)
    wd.close()
    for song_name in songs:
        try:
            url = get_url(song_name)
            download(url)
        except:
            print(f"{song_name} failed to download.")
            continue
