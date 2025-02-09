import pygame
import saveloader as sl

pygame.mixer.init()

def sound_play(sound: str, volume: float, repeat: int = 0):
    sl.create_savefolder("audio")
    audio = pygame.mixer.Sound(f"audio/{sound}.mp3")
    audio.set_volume(volume)
    audio.play(loops=repeat)

def sound_stop():
    pygame.mixer.stop()