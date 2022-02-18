import os
from random import randint

MUSIC_DIR = 'music/'


def get_music_list():
    tracks = os.listdir(MUSIC_DIR)
    return tracks


def get_random_music(full_path=False):
    music_list = get_music_list()
    music_name = music_list[randint(0, len(music_list) - 1)]
    if full_path:
        music_name = MUSIC_DIR + music_name
    return music_name
