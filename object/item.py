# item.py
# 这个模块用于维护掉落的道具

import pygame
from math import *

from utility import globe

global itstatus
itstatus = {"normal": 0, "fly": 1}
# normal: 通常的下落状态
# fly: 移动到了自机周围, 被自机吸引

global rsource
global player


class SPowerItem(object):
    # 小灵力(火力)道具
    def __init__(self, point):
        self.vx = 0
        self.vy = 0
        self.image = rsource[0][0]
        self.rect = self.image.get_rect()
        self.rect.center = point
        self.status = itstatus["normal"]
        self.frame = 0

    def buffer(self):
        # 每个道具加5灵力
        if globe.scgame.player.power < 495:
            player.power += 5
        else:
            player.power = 500
            globe.scgame.score += 5


class LPowerItem(object):
    # 大灵力(火力)道具
    def __init__(self, point):
        self.vx = 0
        self.vy = 0
        self.image = rsource[2][1]
        rc = self.image.get_rect()
        rc.width = int(rc.width * 0.7)
        rc.height = int(rc.height * 0.7)
        # 贴图放大, 与小P进行区分
        self.image = pygame.transform.scale(self.image, rc.size)
        self.rect = self.image.get_rect()
        self.rect.center = point
        self.status = itstatus["normal"]
        self.frame = 0

    def buffer(self):
        # 每个道具增加100灵力
        if globe.scgame.player.power < 400:
            player.power += 100
        else:
            player.power = 500
            globe.scgame.score += 100


class PointItem(object):
    # 得点道具
    def __init__(self, point):
        self.vx = 0
        self.vy = 0
        self.image = rsource[0][1]
        self.rect = self.image.get_rect()
        self.rect.center = point
        self.status = itstatus["normal"]
        self.frame = 0

    def buffer(self):
        # 每个得点道具可以增加100分
        globe.scgame.score += 100


class LifeItem(object):
    # 1up道具
    def __init__(self, point):
        self.vx = 0
        self.vy = 0
        self.image = rsource[3][0]
        self.rect = self.image.get_rect()
        self.rect.center = point
        self.status = itstatus["normal"]
        self.frame = 0

    def buffer(self):
        # 获得一个残机
        player.life += 1
        globe.destiny.msManager.play_SE("extend")


class CleanBlItem(object):
    # 消弹道具(由于boom等原因造成消弹后弹幕变成的道具)
    def __init__(self, point):
        self.vx = 0
        self.vy = 0
        self.image = rsource[3][1]
        self.rect = self.image.get_rect()
        self.rect.center = point
        self.status = itstatus["normal"]
        self.frame = 0

    def buffer(self):
        # 每个道具可以增加500分
        globe.scgame.score += 500


class ItemManager(object):

    def __init__(self):
        global rsource
        global player
        rsource = globe.destiny.rsManager.image["resource"]
        player = globe.scgame.player

        self.item = set()
        self.speed = 1
        self.fspeed = 10

    def create(self, itype, point):
        # itype(item type): 道具种类
        # point: 坐标
        tp = itype(point)
        if tp.rect.right >= globe.playrc.right:
            tp.rect.right = globe.playrc.right
        if tp.rect.left <= globe.playrc.left:
            tp.rect.left = globe.playrc.left
        # 防止坐标溢出, 保持在屏幕内
        self.item.add(tp)

    def update(self):
        tmp = []
        for i in self.item:
            if i.status == itstatus["normal"]:
                # 维护道具的正常下落
                if i.frame <= 60:
                    speed = self.speed * (-1)
                else:
                    speed = self.speed
                i.rect.top += speed
                if i.rect.colliderect(globe.scgame.player.rect):
                    i.buffer()
                    tmp.append(i)
                if i.rect.top > globe.playrc.bottom:
                    tmp.append(i)
                if i.rect.left < globe.playrc.left or i.rect.right > globe.playrc.right:
                    tmp.append(i)
                i.frame += 1
            elif i.status == itstatus["fly"]:
                # 维护道具被自机的吸引
                dx = player.point[0] - i.rect.centerx
                dy = player.point[1] - i.rect.centery
                dis = sqrt(dx ** 2 + dy ** 2)
                if dis == 0:
                    dis = 0.0001
                i.vx = int(self.fspeed * dx / dis)
                i.vy = int(self.fspeed * dy / dis)
                i.rect.left += i.vx
                i.rect.top += i.vy
                if i.rect.collidepoint(player.point):
                    i.buffer()
                    if i not in tmp:
                        tmp.append(i)
        for i in tmp:
            # 消除无效道具
            try:
                self.item.remove(i)
            except Exception as e:
                continue

    def getitem(self):
        # 吸收得点, 这里使用打tag的形式实现.
        for i in self.item:
            i.status = itstatus["fly"]

    def draw(self, screen):
        for i in self.item:
            screen.blit(i.image, i.rect)
