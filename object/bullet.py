# bullet.py
# 这个模块用来维护子弹类

import pygame

from math import *

from utility import globe
from render import cache
from object import item

global plpoint
played_se = False


class EnemyBullet(object):
    def __init__(self, bltype, orbit):
        self.bltype = bltype
        self.orbit = orbit
        self.ungrazed = True


class BulletType(object):
    def __init__(self, img, area):
        self.image = img
        self.area = area
        self.rect = img.get_rect()


def bl_inter_collide(embullet):
    global plpoint
    blpoint = embullet.orbit.point
    area = embullet.bltype.area

    # 类型自适应
    if type(area) == float or type(area) == int:
        if ((blpoint[0] - plpoint[0]) ** 2 + (blpoint[1] - plpoint[1]) ** 2) < area ** 2:
            return True
    else:
        theta = embullet.orbit.theta
        if type(area) == pygame.Rect:
            rctuple = (area.left, area.top, area.width, area.height)
        else:
            rctuple = area
        disx = plpoint[0] - blpoint[0]
        disy = plpoint[1] - blpoint[1]
        if abs(cos(theta / 180.0 * pi) * disx + sin(theta / 180.0 * pi) * disy) < rctuple[3] / 2 and abs(
                sin(theta / 180.0 * pi) * disx - cos(theta / 180.0 * pi) * disy) < rctuple[2] / 2:
            return True
    return False


def bl_inter_real_graze(embullet: EnemyBullet):
    # 疯狂擦弹的时候撞可能无 biu 音效, 所以控制每帧只播一次擦弹音效
    global played_se
    global plpoint
    globe.scgame.graze += 1
    globe.scgame.score += 100
    embullet.ungrazed = False
    if globe.scgame.player.status != globe.cstatus["hit"] and not played_se:
        globe.destiny.msManager.play_SE("graze")
        globe.scgame.score += 20
        played_se = True
    # 显示擦弹特效
    if globe.scgame.player.status != globe.cstatus["hit"]:
        globe.scgame.anManager.grazeFX(plpoint[0], plpoint[1])


def bl_inter_check_graze(embullet: EnemyBullet):
    # 检测擦弹, 暂定 15 像素可以擦弹
    grazedis = 15
    global plpoint
    blpoint = embullet.orbit.point
    area = embullet.bltype.area

    # 根据子弹类型 (圆形/矩形) 进行对应检测
    if type(area) == float or type(area) == int:
        dis2 = (blpoint[0] - plpoint[0]) ** 2 + (blpoint[1] - plpoint[1]) ** 2
        if dis2 < (area + grazedis) ** 2:
            if embullet.ungrazed:
                bl_inter_real_graze(embullet)
        elif dis2 >= (area + (grazedis << 2)) ** 2:
            embullet.ungrazed = True
        return

    theta = embullet.orbit.theta
    if type(area) == pygame.Rect:
        rctuple = (area.left, area.top, area.width, area.height)
    else:
        rctuple = area

    disx = plpoint[0] - blpoint[0]
    disy = plpoint[1] - blpoint[1]
    left_right = cos(theta / 180.0 * pi) * disx + sin(theta / 180.0 * pi) * disy
    top_bottom = sin(theta / 180.0 * pi) * disx - cos(theta / 180.0 * pi) * disy
    if abs(left_right) < rctuple[3] / 2 + grazedis and abs(top_bottom) < rctuple[2] / 2 + grazedis:
        if embullet.ungrazed:
            bl_inter_real_graze(embullet)
    elif abs(left_right) >= rctuple[3] / 2 + (grazedis << 2) and abs(top_bottom) >= rctuple[2] / 2 + (grazedis << 2):
        embullet.ungrazed = True


def bl_inter_outscr(embullet):
    # 子弹出界
    blpoint = embullet.orbit.point
    if not globe.playrc.inflate(50, 50).collidepoint(blpoint):
        return True


class BulletManager(object):

    def __init__(self):
        self.time = 0

        self.plimg = []

        # 自机弹幕
        self.plimg.append(cache.cache_set_alpha(cache.cache_rotate(globe.destiny.rsManager.anime["ziji"][5], 90), 128))
        self.plimg.append(cache.cache_set_alpha(cache.cache_rotate(globe.destiny.rsManager.anime["ziji"][6], 90), 128))
        self.plimg.append(cache.cache_set_alpha(cache.cache_flip(self.plimg[1]), 128))

        self.plbullet = []  # (rect,id)
        self.plrc = self.plimg[0].get_rect()
        self.plspeed = 32

        self.enbullet = set()

        global plpoint
        plpoint = globe.scgame.player.point

    def create_plbl(self, point, bltype):
        tp = self.plrc.copy()
        tp.midbottom = point
        tp.top += self.plspeed
        self.plbullet.append((tp, bltype))

    def create_enbl(self, bltype, orbit):
        self.enbullet.add(EnemyBullet(bltype, orbit))

    def update(self):
        global played_se
        global plpoint
        enbl_tmp = []
        played_se = False
        for i in self.plbullet:
            i[0].top -= self.plspeed
            if i[0].bottom < globe.playrc.top:
                self.plbullet.remove(i)

        if globe.scgame.player.status == globe.cstatus["sc"]:
            for i in self.enbullet:
                i.orbit.update(i.bltype)
                if bl_inter_outscr(i):
                    enbl_tmp.append(i)
        else:
            for i in self.enbullet:
                if bl_inter_collide(i):
                    enbl_tmp.append(i)
                    globe.scgame.player.hit()
                else:
                    i.orbit.update(i.bltype)
                    if bl_inter_outscr(i):
                        enbl_tmp.append(i)
                bl_inter_check_graze(i)

        for i in enbl_tmp:
            self.enbullet.remove(i)

        self.time += 1

    def draw(self, screen):
        for i in self.plbullet:
            screen.blit(self.plimg[i[1]], i[0])

        for i in self.enbullet:
            if i.orbit.theta != 0:
                tpimg = cache.cache_rotate(i.bltype.image, i.orbit.theta)
                tprc = tpimg.get_rect()
            else:
                tpimg = i.bltype.image
                tprc = tpimg.get_rect()
            tprc.center = i.orbit.point
            screen.blit(tpimg, tprc)

    def clear_enbl(self):
        for i in self.enbullet:
            globe.scgame.itManager.create(item.CleanBlItem, i.orbit.point)
        # 造成全局伤害
        for i in globe.scgame.enManager.enemy:
            if i.health * 0.2 <= 2000:
                i.health -= 2000
            else:
                i.health *= 0.8
        self.enbullet.clear()
