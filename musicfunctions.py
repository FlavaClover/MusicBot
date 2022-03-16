from random import randint
import csv

MUSIC_DIR = 'music/'


def get_all_music(only_name=False):
    music_list = []

    with open(MUSIC_DIR + 'music.csv', 'r', newline='') as csvfile:

        music_reader = csv.reader(csvfile, delimiter=';')
        for i in music_reader:
            music_list.append(i)

    music_list.remove(music_list[0])
    if only_name:
        for i in range(len(music_list)):
            music_list[i] = music_list[i][0] + ' - ' + music_list[i][1]

    return music_list


def get_random_music(full_path=False):
    music_list = get_all_music(only_name=True)
    print(music_list)
    music_name = music_list[randint(0, len(music_list) - 1)] + '.mp3'

    if full_path:
        music_name = MUSIC_DIR + music_name

    return music_name


def get_current_music(name_music: str, full_path=False):
    all_music = get_all_music()

    for i in all_music:
        if name_music == i[0] + ' - ' + i[1]:
            name = i[0] + ' - ' + i[1] + '.mp3'
            if full_path:
                name = MUSIC_DIR + name
            return name


def get_music_by_genre(genre: str, full_path=False):
    music_list = list()

    for i in get_all_music():
        if i[2] == genre:
            name = i[0] + ' - ' + i[1] + '.mp3'
            if full_path:
                name = MUSIC_DIR + name
            music_list.append(name)

    return music_list



