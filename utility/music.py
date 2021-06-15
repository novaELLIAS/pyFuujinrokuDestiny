import pygame
from utility import globe

global se


class SoundManager(object):

    def __init__(self):
        global se
        global bgm
        se = globe.destiny.rsManager.se

    def play_SE(self, file, volume=0.1):
        # 播放SE
        global se
        se[file].set_volume(volume)
        se[file].play()

    def play_BGM(self, file, volume=0.2):
        # 播放BGM
        global bgm
        pygame.mixer.music.load(globe.destiny.rsManager.bgm[file])
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)

    def pause(self):
        pygame.mixer.music.pause()

    def unpause(self):
        pygame.mixer.music.unpause()

    def stop(self):
        pygame.mixer.music.stop()
