# game.py
# 游戏流程控制

import pygame
from pygame.locals import *
import sys

import player
import tama
import background
import globe
import item
import animation
import bullet
import orbit
import enemy
import dialogue
import effect

from hud import *

from scene import menu

import level1


class Scene_Game(object):

    def __init__(self):
        # 各种元素初始化
        globe.scgame = self
        self.rs = globe.destiny.rsManager

        globe.playrc = Rect(32, 16, 384, 448)

        self.hud = Hud()
        self.time = -60

        self.player = player.Player()
        self.player.power = 200
        self.bgManager = background.BackgroundManager()
        self.itManager = item.ItemManager()
        self.tmManager = tama.TamaManager()
        self.blManager = bullet.BulletManager()
        self.anManager = animation.AnimeManager()
        self.enManager = enemy.EnemyManager()
        self.fxManager = effect.EffectManager()

        self.txplayer = dialogue.TextPlayer()

        level1.init()

        globe.destiny.msManager.stop()
        globe.destiny.msManager.play_BGM("lv1")

        self.score = 0
        self.graze = 0
        self.hiscore = globe.hiscore
        print(globe.hiscore)

        self.pause = False
        self.timestop = False
        globe.BOSSING = False

    def stop(self):
        self.pause = True

    def start(self):
        self.pause = False

    def tstop(self):
        self.timestop = True

    def tstart(self):
        self.timestop = False

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F4 and event.mod == pygame.KMOD_LALT:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_ESCAPE:
                    # 处理ESC暂停
                    globe.destiny.msManager.play_SE("pause")
                    globe.destiny.msManager.pause()
                    globe.destiny.call(menu.Scene_Menu)

                elif event.key == K_z and self.timestop:
                    # 对于dialogue: 下一个对话
                    self.txplayer.command("next")

        if not self.pause:
            # 流程更新
            self.bgManager.update()
            self.player.update()
            self.itManager.update()
            self.tmManager.update()
            self.blManager.update()
            self.anManager.update()
            self.enManager.update()
            level1.update(self.time)
            if not self.timestop:
                self.time += 1
            else:
                self.txplayer.update()

    def draw(self, screen):
        screen.fill((255, 255, 255))
        self.bgManager.draw(screen)
        self.fxManager.draw(screen)
        self.itManager.draw(screen)
        self.enManager.draw(screen)
        self.player.draw(screen)
        self.tmManager.draw(screen)
        self.anManager.draw(screen)
        self.blManager.draw(screen)
        self.hud.draw(screen)

        if self.timestop:
            self.txplayer.draw(screen)
