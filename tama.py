# tama.py
# tama(阴阳玉)为设定中的自机攻击道具, 这个模块维护自机火力.

import pygame
from pygame.locals import *

import globe
import cache

global ziji


class TamaManager(object):

    def __init__(self):
        global ziji
        self.rect = []
        self.tmimg = globe.destiny.rsManager.anime["ziji"][4]
        # tmimg(tama image) 提取贴图
        ziji = globe.scgame.player
        for i in range(4):
            self.rect.append(self.tmimg.get_rect())
            # 自机满火力时总共有四颗阴阳玉

    def update(self):
        global ziji
        self.image = cache.cache_rotate(self.tmimg, globe.scgame.time * 2, True)
        # 处理阴阳玉的旋转
        for i in range(4):
            self.rect[i].size = self.image.get_size()
        power = ziji.power
        if ziji.keys[pygame.K_LSHIFT]:
            dis = 18
        else:
            dis = 28
        # 上文为按下左shift键时(低速模式)阴阳玉收缩
        # 下文为自机火力不同, 阴阳玉的数量和位置各不相同.
        if power < 100:
            # 当火力小于100时, 没有阴阳玉.
            pass
        elif power < 200:
            # 当火力在100和200之间时, 有一颗阴阳玉在头顶, 发射封魔针.
            self.rect[0].center = ziji.point
            self.rect[0].top -= dis
        elif power < 300:
            # 当火力在200和300之间时, 有两颗阴阳玉在左右两侧, 发射封魔针.
            self.rect[0].center = ziji.point
            self.rect[0].left -= dis
            self.rect[1].center = ziji.point
            self.rect[1].left += dis
        elif power < 400:
            # 当火力在300和400之间时, 有三颗阴阳玉, 分别在左右和头顶, 发射封魔针.
            self.rect[0].center = ziji.point
            self.rect[0].left -= dis
            self.rect[1].center = ziji.point
            self.rect[1].left += dis
            self.rect[2].center = ziji.point
            self.rect[2].top -= dis
        else:
            # 当火力在400和全盛(500)之间时, 左右各两颗阴阳玉, 发射封魔针.
            self.rect[0].center = ziji.point
            self.rect[0].left -= dis
            self.rect[1].center = ziji.point
            self.rect[1].left += dis
            self.rect[2].center = self.rect[0].center
            self.rect[2].left -= (dis - 10)
            self.rect[3].center = self.rect[1].center
            self.rect[3].left += (dis - 10)

    def draw(self, screen):
        # 将阴阳玉绘制在屏幕上.
        tp = int(ziji.power / 100)
        if tp > 4:
            tp = 4
        # tp为阴阳玉个数.
        for i in range(tp):
            screen.blit(self.image, self.rect[i])
