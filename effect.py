# effect.py
# 这个模块维护粒子特效


from math import cos, sin
import random

import pygame


class Snow:
    x = 0
    y = 0
    r = 0
    vx = 0.0
    vy = 0.0
    tick = 0
    maxtick = 9999
    visible = False
    def init(self):
        self.tick = 0
        self.r = random.randint(1, 2)

    # 更新位置并绘制
    def draw(self, screen: pygame.Surface):
        if not self.visible: return
        self.tick += 1
        self.x += self.vx
        self.y += self.vy
        color = (200, 200, 200)
        pygame.draw.circle(screen, color, (self.x, self.y), self.r, self.r)
        if (self.tick == self.maxtick):
            self.visible = False


class EffectManager:

    # 擦弹时飞溅的粒子, 预先定义防止性能开销
    # `_` 开头的东西不应被外部调用
    _grazeSnowList = list()
    _grazeSnowPtr = 0

    def __init__(self) -> None:
        self._grazeSnowPtr = 0
        for i in range(200):
            self._grazeSnowList.insert(i, Snow())

    def _getGrazeSnow(self) -> Snow:
        snow = self._grazeSnowList[self._grazeSnowPtr]
        self._grazeSnowPtr += 1
        if self._grazeSnowPtr == 200:
            self._grazeSnowPtr = 0
        snow.init()
        return snow

    def hitFX(self, playerx, playery):
        for i in range(100):
            snow = self._getGrazeSnow()
            snow.maxtick = random.randint(30, 40)
            direction = random.randint(0, 359)
            snow.x = playerx
            snow.y = playery
            snow.vx = cos(direction) * random.randint(2, 6)
            snow.vy = sin(direction) * random.randint(2, 6)
            snow.visible = True

    def grazeFX(self, playerx, playery):
        for i in range(4):
            snow = self._getGrazeSnow()
            snow.maxtick = random.randint(10, 20)
            direction = random.randint(0, 359)
            snow.x = playerx
            snow.y = playery
            snow.vx = cos(direction) * 3
            snow.vy = sin(direction) * 3
            snow.visible = True

    def draw(self, screen: pygame.Surface):
        for snow in self._grazeSnowList:
            snow.draw(screen)
