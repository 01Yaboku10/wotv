import pygame
import saveloader as sl
import os
import failsafe as fs
from colorama import Fore, Style, init

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

    if not lists:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} No audio files found...")
        return

    for i, music in enumerate(lists):
        print(f"[{i+1}] {music}")

    while True:
        play = fs.is_int(input("Play music: "))
        if 1 <= play <= len(lists):
            sound_stop()
            sound_play(lists[play-1], 0.2, -1)
            break

def stripper():
    lines = ["ambiance_far_horizions", "ambiance_kyne's_peace", "battle_knight", "battle_solitude", "bogus"]
    categories: set = set()
    music: dict = {"uncategorised": []}
    for line in lines:
        split: list = line.split("_")
        if len(split) == 1:
            categories.add("uncategorised")
            music["uncategorised"].append(split[0].capitalize())
            continue
        category: str = split.pop(0)
        categories.add(category)
        for i in categories:
            if i not in music:
                music[i] = []
        entry: str = ""
        for piece in split:
            entry += f"{piece.capitalize()} "
        music[category].append(entry.strip())
    
    for index, category in enumerate(music):
        print(f"[{index+1}] {category.capitalize()}")
    
    while True:
        choice = input("Play from category [A]ll, [Q]uit: ").upper()
        if choice == "Q":
            return
        elif choice == "A":
            pass
        elif 1 <= int(choice) <= len(music):
            category = 0
            for index, cate in enumerate(music):
                if index == int(choice)-1:
                    category = cate
            print(f"---------={category.capitalize()}=---------")
            for index, track in enumerate(music[category]):
                print(f"[{index+1}] {track}")
            break
