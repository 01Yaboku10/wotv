import pygame
import saveloader as sl
import os
import failsafe as fs

pygame.mixer.init()

def sound_play(sound: str, volume: float, repeat: int = 0):
    sl.create_savefolder("audio")
    sl.create_savefolder("audio/music")
    sl.create_savefolder("audio/spells")
    try:
        audio = pygame.mixer.Sound(f"audio/music/{sound}.mp3")
    except:
        audio = pygame.mixer.Sound(f"audio/spells/{sound}.mp3")
    audio.set_volume(volume)
    audio.play(loops=repeat)

def sound_stop():
    pygame.mixer.stop()

def sound_menu(mode: str = "all"):
    print("---------=Play Music=---------")
    sl.create_savefolder("audio")
    sl.create_savefolder("audio/music")
    sl.create_savefolder("audio/spells")

    ambiance = []
    battle = []
    all = []

    if mode == "all":
        lists = all
    elif mode == "ambiance":
        lists = ambiance
    elif mode == "battle":
        lists = battle
    else:
        lists = all

    iteration = 1
    files = os.listdir("audio/music")
    while iteration <= 2:
        for i, name in enumerate(files):
            if name.startswith("ambiance"):
                ambiance.append(name.removesuffix(".mp3"))
            elif name.startswith("battle"):
                battle.append(name.removesuffix(".mp3"))
            all.append(name.removesuffix(".mp3"))
        files = os.listdir("audio/spells")
        iteration += 1

    for i, music in enumerate(lists):
        print(f"[{i+1}] {music}")

    while True:
        play = fs.is_int(input("Play music: "))
        if 1 <= play <= len(lists):
            sound_stop()
            sound_play(lists[play-1], 0.2, -1)
            break
