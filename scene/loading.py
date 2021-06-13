# loading.py
# 维护加载页面
import threading

import pygame
import sys
import globe
from random import *

maples = []
clock = pygame.time.Clock()


class Scene_Loading(object):

    def __init__(self):

        globe.logonflag = False
        globe.updateflag = False
        globe.getrankflag = False

        globe.destiny.msManager.stop()
        self.screen = pygame.display.set_mode((640, 480))
        self.res = globe.destiny.rsManager.image["loading"]
        self.loading = self.res.subsurface(4, 0, 124, 57)
        self.count = 0
        self.fincount = 100000
        self.unfinflag = True
        # 淡出切换效果
        self.fade = pygame.Surface(globe.destiny.screen.get_size())
        self.fade.fill((0, 0, 0))

        T = threading.Thread(target=self.dbinit)
        T.start()

    def dbinit(self):

        globe.logonflag = True
        globe.updateflag = True
        globe.getrankflag = True

        print(globe.destiny.sync_flag)
        for i in globe.destiny.sync_flag:
            if i == "login":
                globe.logonflag = False
            elif i == "sync":
                globe.updateflag = False
            elif i == "getrank":
                globe.getrankflag = False

        globe.destiny.dbManager.asyncprocess()

    def draw(self, screen):
        screen.blit(self.fade, (0, 0))
        for maple in maples:
            now = maple.image
            nowRect = now.get_rect()
            new = pygame.transform.rotate(now, maple.rinit)
            newRect = new.get_rect(center=nowRect.center)
            newRect.center = (maple.rect.x, maple.rect.y)
            screen.blit(new, newRect)
        screen.blit(self.loading, [460, 380])
        if globe.logonflag and globe.updateflag and globe.getrankflag:
            if self.unfinflag:
                self.fincount = self.count
                self.unfinflag = False
            self.fade.set_alpha((self.count - self.fincount) * 12)  # 对遮罩进行透明化
            screen.blit(self.fade, (0, 0))

    def update(self):
        pygame.init()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            else:
                pass
        if (self.count % 13 == 0) and (len(maples) <= 10):
            maple = Maple()
            maples.append(maple)
        maple_update()
        self.count += 1
        if globe.logonflag and globe.updateflag and globe.getrankflag and (self.count - self.fincount >= 30):
            globe.destiny.goto(globe.destiny.navigate_to)


class Maple(object):
    # 枫树叶子随机飘落

    def __init__(self):
        self.xspeed = 2 * random()
        self.yspeed = 1
        self.rinit = 1
        self.rspeed = randint(1, 6)
        self.image = globe.destiny.rsManager.image["loading"].subsurface(0, 64, 33, 33)
        self.rect = self.image.get_rect()
        self.rect.x = randint(460, 520)
        self.rect.y = 360.0


def maple_update():
    for maple in maples:
        maple.rinit += maple.rspeed
        maple.rect.y += maple.yspeed
        maple.rect.x += maple.xspeed
        if (maple.rect.y >= 440) or (maple.rect.x >= 590) or (maple.rect.x <= 460):
            maples.remove(maple)
