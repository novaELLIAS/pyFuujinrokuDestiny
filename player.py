# player.py
# 这个模块主要维护自机的相关参数

import pygame
from pygame.locals import *

import globe
import cache
import item
from scene import gameover
from math import *

global resource
global cstatus
global canime


class Player(object):

    def __init__(self):
        global resource
        resource = globe.destiny.rsManager
        self.playrc = globe.playrc
        self.point = [224.0, 450.0]
        # 自机的初始位置始终在屏幕下方的正中央
        self.rect = Rect(0, 0, 10, 10)
        # 注意: 自机的判定区域仅限判定点

        global cstatus
        global canime
        cstatus = {"normal": 0, "wudi": 1, "crash": 2, "sc": 3, "scwudi": 4, "hit": 5}
        # 状态: 通常状态, Miss, 撞后无敌状态(放bomb), 扔雷状态, 扔雷后无敌状态, 被弹

        self.status = cstatus["normal"]

        globe.cstatus = cstatus

        canime = {"stay": resource.anime["ziji"][0], "toleft": resource.anime["ziji"][1],
                  "toright": resource.anime["ziji"][2], "focus": resource.anime["ziji"][3]}
        # 自机的几种动画状态: 不动, 向左移动, 向右移动, 判定点(低速模式)

        self.anime = canime["stay"]
        # anime, 动画状态
        self.aindex = 0
        # anime index, 动画的编号
        self.power = 200
        # 灵力
        self.life = 3
        # 残机数量
        self.frame = 0
        # 帧数计数器
        self.tcount = 0
        # 事件计时器, 用于决死等事件的时钟

    def fire(self):
        # 开火射击
        if not globe.scgame.timestop:
            tm = globe.scgame.tmManager  # tama manager
            bl = globe.scgame.blManager  # bullet manager
            bl.create_plbl(self.rect.inflate(-12, -8).topleft, 0)
            bl.create_plbl(self.rect.inflate(-12, -8).topright, 0)
            tp = self.power / 100
            if tp >= 5:
                tp = 4
            for i in range(int(tp)):
                bl.create_plbl(tm.rect[i].center, 1)
                bl.create_plbl(tm.rect[i].center, 2)

    def throwbomb(self):
        # 扔雷
        if self.power >= 100 and self.status != cstatus["sc"] and self.status != cstatus[
            "scwudi"] and not globe.scgame.timestop:
            self.power -= 100
            self.status = cstatus["sc"]
            globe.scgame.itManager.getitem()
            globe.destiny.msManager.play_SE("wudi")

    def hit(self):
        # 撞了
        if self.status == cstatus["normal"]:
            globe.destiny.msManager.play_SE("miss")
            self.tcount = 0
            self.status = cstatus["hit"]

    def miss(self):
        # 撞了之后没决死, miss
        if self.status == cstatus["hit"]:
            globe.scgame.anManager.hitFX(self.point[0], self.point[1])
            globe.scgame.blManager.clear_enbl()
            rc = self.rect.copy()
            rc.left -= 20
            globe.scgame.itManager.create(item.LPowerItem, rc.topleft)
            rc.left += 20
            globe.scgame.itManager.create(item.LPowerItem, rc.midtop)
            rc.left += 20
            globe.scgame.itManager.create(item.LPowerItem, rc.topright)

            self.status = cstatus["crash"]
            self.tmppd = [0, 0]
            self.tmppd[0] = self.point[0]
            self.tmppd[1] = self.point[1]
            self.rect.midtop = self.playrc.midbottom
            self.point[0] = self.rect.centerx
            self.point[1] = self.rect.centery
            self.tcount = 0
            self.life -= 1
            self.power -= 200
            if self.power <= 0:
                self.power = 0

    def isThough(self) -> bool:
        return self.status == cstatus["wudi"] or self.status == cstatus["sc"] or self.status == cstatus["scwudi"]

    def move(self):
        # 处理自机状态变化(键位操作)

        keys = self.keys

        if keys[pygame.K_z]:
            self.fire()

        if keys[pygame.K_x]:
            self.throwbomb()

        if keys[pygame.K_LSHIFT]:
            # 低速模式
            self.speed = 1.5
        else:
            self.speed = 8

        if (keys[pygame.K_DOWN] or keys[pygame.K_UP]) and (keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]):
            # 对角线方向移动, 确保实际运动速度相同(当卡底板时也可以同时按住"下"来进一步减速)
            self.speed /= sqrt(2)

        if keys[pygame.K_DOWN]:
            self.point[1] += self.speed
        if keys[pygame.K_UP]:
            self.point[1] -= self.speed

        if keys[pygame.K_RIGHT] and keys[pygame.K_LEFT]:
            if self.anime != canime["stay"]:
                self.anime = canime["stay"]
                self.aindex = 0
        elif keys[pygame.K_RIGHT]:
            if self.anime != canime["toright"]:
                self.anime = canime["toright"]
                self.aindex = 0
            self.point[0] += self.speed

        elif keys[pygame.K_LEFT]:
            if self.anime != canime["toleft"]:
                self.anime = canime["toleft"]
                self.aindex = 0
            self.point[0] -= self.speed

        if (not keys[pygame.K_LEFT]) and (not keys[pygame.K_RIGHT]):
            if self.anime != canime["stay"]:
                self.anime = canime["stay"]
                self.aindex = 0

        self.rect.size = self.anime[self.aindex].get_size()
        self.rect.center = (int(self.point[0]), int(self.point[1]))

        if self.rect.top < self.playrc.top:
            self.rect.top = self.playrc.top
            self.point[1] = self.rect.centery
        elif self.rect.bottom > self.playrc.bottom:
            self.rect.bottom = self.playrc.bottom
            self.point[1] = self.rect.centery

        if self.rect.left < self.playrc.left:
            if self.isThough():
                self.rect.right = self.playrc.right
                globe.destiny.msManager.play_SE("select")
            else:
                self.rect.left = self.playrc.left
            self.point[0] = self.rect.centerx
        elif self.rect.right > self.playrc.right:
            if self.isThough():
                self.rect.left = self.playrc.left
                globe.destiny.msManager.play_SE("select")
            else:
                self.rect.right = self.playrc.right
            self.point[0] = self.rect.centerx

        if self.rect.top < 100:
            # 上线收点, 收点线为距离顶端100单位处
            globe.scgame.itManager.getitem()

        # 自机动画循环播放
        if self.frame % 6 == 0:
            self.aindex += 1

        if self.aindex >= len(self.anime):
            if self.anime == canime["stay"]:
                self.aindex = 0
            else:
                self.aindex -= 4

    def update(self):

        self.keys = pygame.key.get_pressed()

        if self.power > 500:
            self.power = 500

        if self.status == cstatus["hit"]:
            # 如果撞了, 处理决死(20帧)
            if self.tcount >= 20:
                self.miss()
            else:
                self.tcount += 1

        if self.status != cstatus["crash"]:
            self.move()
        else:
            self.tcount += 1
            if self.life < 0 and self.tcount >= 20:
                # 没有残机了, 结束游戏
                globe.hiscore = globe.scgame.hiscore
                globe.destiny.call(gameover.Scene_GameOver)
            if self.tcount <= 60:
                self.point[1] -= 1
            else:
                self.status = cstatus["wudi"]
                self.tcount = 0

        if self.status == cstatus["wudi"]:
            # miss后无敌状态
            self.tcount += 1
            if self.tcount > 300:
                self.status = cstatus["normal"]
                self.tcount = 0
        elif self.status == cstatus["sc"]:
            # 扔雷和扔雷后的无敌状态
            self.tcount += 1
            if self.tcount > 360:
                self.status = cstatus["scwudi"]
                globe.scgame.blManager.clear_enbl()
                self.tcount = 0
        elif self.status == cstatus["scwudi"]:
            # 扔雷后的无敌状态
            self.tcount += 1
            if self.tcount > 180:
                self.status = cstatus["normal"]
                self.tcount = 0

        self.frame += 1

    def draw(self, screen):

        self.rect.centerx = int(self.point[0])
        self.rect.centery = int(self.point[1])

        if self.status != cstatus["normal"] and self.status != cstatus["hit"]:
            # 除以上两种情况外, 需要对自机设定透明度.
            tmp = cache.cache_set_alpha(self.anime[self.aindex], int((self.frame % 15) * 60 / 15) + 100, True)
            tmp = cache.cache_set_mask(tmp, (100, 0, 100, 40), True)
            screen.blit(tmp, self.rect)
        else:
            screen.blit(self.anime[self.aindex], self.rect)

        tmp = cache.cache_rotate(canime["focus"], self.frame, True)
        tprc = tmp.get_rect()
        if self.keys[pygame.K_LSHIFT]:
            # 绘制低速模式
            if self.status != cstatus["crash"]:
                tprc.center = self.rect.center
                screen.blit(tmp, tprc)
        if self.status == cstatus["crash"]:
            tprc.center = self.tmppd
            screen.blit(tmp, tprc)
