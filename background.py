# background.py
# 维护背景

import pygame
from pygame.locals import *

import globe
import cache


class BackgroundManager(object):

    def __init__(self):
        self.time = 0
        self.sc = False
        self.tt = 0

        # 一种水(深色)
        bg3 = globe.destiny.rsManager.image["bg3"]
        self.bg3 = pygame.Surface((512, 1024), flags=SRCALPHA)
        self.bg3.blit(bg3, (0, 0))
        self.bg3.blit(bg3, (0, 512))   # 拼接
        self.bg3 = self.bg3.convert()  # 渲染加速
        self.v3 = 0.3                  # 移速压缩比

        # 另一种水(浅色)
        wa = globe.destiny.rsManager.image["bg2"]
        wa = wa.convert()
        wa.set_alpha(63)
        self.wa = pygame.Surface((640, 640), flags=SRCALPHA)
        x = 0
        while x < 640:  # 还是拼接
            y = 0
            while y < 640:
                self.wa.blit(wa, (x, y))
                y += 128
            x += 128
        self.war = pygame.transform.flip(self.wa, 1, 1)
        self.vw = 0.5

        # 岸边
        pic = globe.destiny.rsManager.image["bg1"]
        pl = pic.subsurface(0, 0, 128, 256)
        pr = pic.subsurface(128, 0, 128, 256)
        self.pl = pygame.Surface((128, 768), flags=SRCALPHA)
        self.pr = pygame.Surface((128, 768), flags=SRCALPHA)
        y = 0
        while y < 768:
            self.pl.blit(pl, (0, y))
            self.pr.blit(pr, (0, y))
            # 左右两岸
            y += 256
        self.vl = 0.5

        # 树
        bg4 = globe.destiny.rsManager.image["bg4"]
        self.bg4 = pygame.Surface((256, 1200), flags=SRCALPHA)
        self.bg4.blit(bg4, (0, 0))
        self.bg4.blit(bg4, (0, 600))
        self.bg4 = pygame.transform.flip(self.bg4, 1, 1)
        self.v4 = 0.7

        # 深蓝渐变(用于boss战)
        bg5 = globe.destiny.rsManager.image["bg5"]
        bg5 = pygame.transform.scale(bg5, (384, 384))
        bg5.convert()
        self.bg5 = pygame.Surface((384, 1152))
        y = 0
        while y < 1152:
            self.bg5.blit(bg5, (0, y))
            y += 384
        self.v5 = 0.3

    def update(self):
        self.time += 1

    def background_change(self, scene):
        # 基于不同scene更换背景
        self.sc = scene
        self.tt = self.time

    def draw(self, screen):

        # 绘制扔雷蒙版
        if globe.scgame.player.status == globe.cstatus["sc"]:
            color = (150, 150, 150)
        else:
            color = (0, 0, 0)

        # 绘制四种背景的移动
        t = (int(self.time * self.v3)) % 512
        tmp = cache.cache_set_mask(self.bg3, color, True)
        screen.blit(tmp.subsurface(0, 512 - t, 384, 448), (32, 16))

        t = (int(self.time * self.vw)) % 128
        tmp = cache.cache_set_mask(self.wa, color, True)
        screen.blit(tmp.subsurface(128 - t, 128 - t, 384, 448), (32, 16))
        tmp = cache.cache_set_mask(self.war, color, True)
        screen.blit(tmp.subsurface(t, 128 - t, 384, 448), (32, 16))

        t = (int(self.time * self.vl)) % 256
        tmp = cache.cache_set_mask(self.pl, color, True)
        screen.blit(tmp.subsurface(0, 256 - t, 128, 448), (32, 16))
        tmp = cache.cache_set_mask(self.pr, color, True)
        screen.blit(tmp.subsurface(0, 256 - t, 128, 448), (288, 16))

        t = (int(self.time * self.v4)) % 600
        tmp = cache.cache_set_mask(self.bg4, color, True)
        screen.blit(tmp.subsurface(0, 600 - t, 256, 448), (160, 16))

        if self.sc:  # boss战场景
            t = (int((self.time - self.tt) * self.v5)) % 384
            x = (self.time - self.tt) / 5
            if x > 20:
                x = 20
            self.bg5.set_alpha(int(x * 12.75))
            screen.blit(self.bg5.subsurface(0, 384 - t, 384, 448), (32, 16), None)
            if globe.scgame.player.status == globe.cstatus["sc"]:
                screen.fill((150, 150, 150), globe.playrc)
