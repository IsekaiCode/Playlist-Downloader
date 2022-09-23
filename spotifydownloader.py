from __future__ import unicode_literals
import youtube_dl

import urllib.request

import os
import re
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains


def find_songs(wd):
    # get song names from playlist

    class_name = "gvLrgQXBFVW6m9MscfFA"
    slider = wd.find_element(
        By.XPATH, '//*[@id="main"]/div/div[2]/div[3]/div[1]/div[2]/div[4]/div/div')

    songs = set()
    action = ActionChains(wd)

    while True:
        max_value = len(songs)

        # scroll action
        action.drag_and_drop_by_offset(slider, 0, 300)
        action.perform()
        time.sleep(3)

        names = wd.find_elements(By.CLASS_NAME, class_name)
        for name in names:
            songs.add(name.text.replace('\n', ' '))
        if max_value == len(songs):
            wd.close()
            print(f"found { len(songs) } songs.")
            return songs


def get_url(name: str):
    # transform song name to song url

    search_keyword = name.replace(" ", "+")
    html = urllib.request.urlopen(
        f"https://www.youtube.com/results?search_query={search_keyword}")
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode('utf-8'))
    video_url = f"https://www.youtube.com/watch?v={video_ids[0]}"
    return video_url


def download_url(url: str):
    # download songs from urls

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'./songs/%(title)s.%(ext)s'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def main(url: str, wd_path='./chromedriver.exe'):
    # dont forget to update your chromedriver

    if url.find('https://open.spotify.com') != 1:

            # Web driver
            s = Service(wd_path)
            options = webdriver.ChromeOptions()
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            wd = webdriver.Chrome(service=s, options=options)
            wd.get(url)

            # Run
            time.sleep(3)
            songs = find_songs(wd)

            for song_name in songs:

                try:
                    song_url = get_url(song_name)
                    download_url(song_url)

                except KeyboardInterrupt:
                    print('Interrupted')
                    try:
                        sys.exit(0)
                    except SystemExit:
                        os._exit(0)

                except:
                    print(f"{song_name} failed to download.")
                    with open('failed_downloads.txt', 'w') as f:
                        f.write(f'failed... {song_name}\n')
                    continue

